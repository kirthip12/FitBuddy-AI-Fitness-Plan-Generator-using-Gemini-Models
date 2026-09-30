from __future__ import annotations

from datetime import datetime

from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Request
)

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)
from .gemini_generator import (
    generate_workout_gemini
)
from .models import User, Plan
from .schemas import (
    UserInput,
    FeedbackRequest,
    GenerateResponse
)
from .updated_plan import (
    update_workout_plan
)


router = APIRouter()

templates = Jinja2Templates(
    directory="templates"
)


def save_generated_plan(
    db: Session,
    payload: UserInput
):

    existing_user = db.scalar(
        select(User).where(
            User.user_id == payload.user_id
        )
    )

    if existing_user:

        user = existing_user

        data = payload.model_dump()

        for key, value in data.items():
            setattr(
                user,
                key,
                value
            )

    else:

        user = User(
            **payload.model_dump()
        )

        db.add(user)

    workout_plan, workout_mode = (
        generate_workout_gemini(
            payload.name,
            payload.age,
            payload.weight,
            payload.goal,
            payload.intensity,
            payload.experience_level
        )
    )

    nutrition_tip, tip_mode = (
        generate_nutrition_tip_with_flash(
            payload.goal
        )
    )

    plan = db.scalar(
        select(Plan).where(
            Plan.user_id == payload.user_id
        )
    )

    if plan:

        plan.original_plan = workout_plan
        plan.updated_plan = None
        plan.feedback = None
        plan.nutrition_tip = nutrition_tip
        plan.updated_at = None

    else:

        plan = Plan(
            user_id=payload.user_id,
            original_plan=workout_plan,
            nutrition_tip=nutrition_tip
        )

        db.add(plan)

    db.commit()

    db.refresh(user)
    db.refresh(plan)

    if (
        workout_mode == "gemini"
        or tip_mode == "gemini"
    ):
        mode = "gemini"
    else:
        mode = "demo"

    return user, plan, mode


# -----------------------------------
# HOME PAGE
# -----------------------------------

@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title":
            "FitBuddy - AI Fitness Plan Generator"
        }
    )


# -----------------------------------
# HTML WORKOUT GENERATION
# -----------------------------------

@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout_form(

    request: Request,

    name: str = Form(...),

    user_id: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    experience_level: str = Form(
        "beginner"
    ),

    db: Session = Depends(get_db)
):

    try:

        payload = UserInput(

            name=name,

            user_id=user_id,

            age=age,

            weight=weight,

            goal=goal,

            intensity=intensity,

            experience_level=experience_level
        )

    except Exception as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    user, plan, mode = (
        save_generated_plan(
            db,
            payload
        )
    )

    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "title":
            "Your FitBuddy Plan",

            "user":
            user,

            "plan":
            plan,

            "workout_plan":
            plan.original_plan,

            "nutrition_tip":
            plan.nutrition_tip,

            "mode":
            "Gemini"
            if mode == "gemini"
            else "Demo",

            "message":
            None
        }
    )


# -----------------------------------
# FEEDBACK FORM
# -----------------------------------

@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback_form(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)
):

    try:

        data = FeedbackRequest(
            user_id=user_id,
            feedback=feedback
        )

    except Exception as exc:

        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    user = db.scalar(
        select(User).where(
            User.user_id == data.user_id
        )
    )

    plan = db.scalar(
        select(Plan).where(
            Plan.user_id == data.user_id
        )
    )

    if not user or not plan:

        raise HTTPException(
            status_code=404,
            detail="User or workout plan not found."
        )

    revised_plan, mode = (
        update_workout_plan(

            plan.original_plan,

            data.feedback,

            user.goal,

            user.intensity,

            user.experience_level
        )
    )

    plan.updated_plan = revised_plan

    plan.feedback = data.feedback

    plan.updated_at = datetime.utcnow()

    db.commit()

    db.refresh(plan)

    return templates.TemplateResponse(

        request=request,

        name="result.html",

        context={

            "title":
            "Updated FitBuddy Plan",

            "user":
            user,

            "plan":
            plan,

            "workout_plan":
            revised_plan,

            "nutrition_tip":
            plan.nutrition_tip,

            "mode":
            "Gemini"
            if mode == "gemini"
            else "Demo",

            "message":
            "Your plan was updated using your feedback."
        }
    )


# -----------------------------------
# ADMIN PAGE
# -----------------------------------

@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    db: Session = Depends(get_db)
):

    users = db.scalars(
        select(User).order_by(
            User.created_at.desc()
        )
    ).all()

    plans = {
        plan.user_id: plan

        for plan in db.scalars(
            select(Plan)
        ).all()
    }

    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={

            "title":
            "FitBuddy Admin Dashboard",

            "users":
            users,

            "plans":
            plans
        }
    )


# -----------------------------------
# API GENERATE WORKOUT
# -----------------------------------

@router.post(
    "/api/generate-workout",
    response_model=GenerateResponse
)
def api_generate_workout(

    payload: UserInput,

    db: Session = Depends(get_db)
):

    user, plan, mode = (
        save_generated_plan(
            db,
            payload
        )
    )

    return GenerateResponse(

        user_id=payload.user_id,

        name=payload.name,

        goal=payload.goal,

        intensity=payload.intensity,

        workout_plan=plan.original_plan,

        nutrition_tip=plan.nutrition_tip,

        mode=mode
    )


# -----------------------------------
# API FEEDBACK
# -----------------------------------

@router.post(
    "/api/submit-feedback"
)
def api_submit_feedback(

    payload: FeedbackRequest,

    db: Session = Depends(get_db)
):

    user = db.scalar(
        select(User).where(
            User.user_id == payload.user_id
        )
    )

    plan = db.scalar(
        select(Plan).where(
            Plan.user_id == payload.user_id
        )
    )

    if not user or not plan:

        raise HTTPException(
            status_code=404,
            detail="User or workout plan not found."
        )

    revised_plan, mode = (
        update_workout_plan(

            plan.original_plan,

            payload.feedback,

            user.goal,

            user.intensity,

            user.experience_level
        )
    )

    plan.updated_plan = revised_plan

    plan.feedback = payload.feedback

    plan.updated_at = datetime.utcnow()

    db.commit()

    return {

        "user_id":
        payload.user_id,

        "updated_plan":
        revised_plan,

        "nutrition_tip":
        plan.nutrition_tip,

        "mode":
        mode
    }


# -----------------------------------
# API USERS
# -----------------------------------

@router.get(
    "/api/users"
)
def api_users(

    db: Session = Depends(get_db)
):

    users = db.scalars(
        select(User).order_by(
            User.created_at.desc()
        )
    ).all()

    plans = {
        plan.user_id: plan

        for plan in db.scalars(
            select(Plan)
        ).all()
    }

    result = []

    for user in users:

        plan = plans.get(
            user.user_id
        )

        result.append({

            "id":
            user.id,

            "user_id":
            user.user_id,

            "name":
            user.name,

            "age":
            user.age,

            "weight":
            user.weight,

            "goal":
            user.goal,

            "intensity":
            user.intensity,

            "experience_level":
            user.experience_level,

            "original_plan":
            plan.original_plan
            if plan else None,

            "updated_plan":
            plan.updated_plan
            if plan else None,

            "feedback":
            plan.feedback
            if plan else None
        })

    return result