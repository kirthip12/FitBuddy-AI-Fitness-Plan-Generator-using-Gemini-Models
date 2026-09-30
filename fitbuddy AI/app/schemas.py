from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    field_validator
)


Goal = Literal[
    "weight loss",
    "muscle gain",
    "general wellness",
    "flexibility"
]

Intensity = Literal[
    "low",
    "medium",
    "high"
]

ExperienceLevel = Literal[
    "beginner",
    "intermediate",
    "advanced"
]


class UserInput(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=120
    )

    user_id: str = Field(
        min_length=2,
        max_length=100
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=20,
        le=500
    )

    goal: Goal

    intensity: Intensity

    experience_level: ExperienceLevel = "beginner"

    @field_validator(
        "name",
        "user_id"
    )
    @classmethod
    def clean_text(cls, value: str):

        value = value.strip()

        if not value:
            raise ValueError(
                "This field cannot be empty."
            )

        return value


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=2,
        max_length=100
    )

    feedback: str = Field(
        min_length=5,
        max_length=2000
    )

    @field_validator(
        "user_id",
        "feedback"
    )
    @classmethod
    def clean_text(cls, value: str):

        return value.strip()


class GenerateResponse(BaseModel):

    user_id: str
    name: str
    goal: str
    intensity: str
    workout_plan: str
    nutrition_tip: str
    mode: str