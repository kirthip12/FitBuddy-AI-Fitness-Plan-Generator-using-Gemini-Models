from __future__ import annotations

import os

from .gemini_client import generate_text
from .gemini_generator import demo_plan


WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-3.8-flash"
)


def update_workout_plan(
    original_plan: str,
    feedback: str,
    goal: str,
    intensity: str,
    experience_level: str
):

    prompt = f"""
You are FitBuddy.

The user already has a 7-day workout plan.

GOAL:
{goal}

INTENSITY:
{intensity}

EXPERIENCE:
{experience_level}


ORIGINAL PLAN:

{original_plan}


USER FEEDBACK:

{feedback}


TASK:

Create a revised 7-day workout plan.

Apply the user's feedback where appropriate.

Keep:
- 7 days
- safe progression
- warm-up
- exercises
- rest
- cooldown
- recovery
- appropriate intensity
- appropriate experience level

Do not:
- diagnose medical conditions
- prescribe medicines
- recommend dangerous exercise
- recommend extreme dieting

Return only the revised plan.
"""

    try:

        result = generate_text(
            prompt,
            WORKOUT_MODEL
        )

        return result, "gemini"

    except Exception:

        result = demo_plan(
            "FitBuddy User",
            goal,
            intensity,
            experience_level
        )

        result += (
            "\n\nUSER FEEDBACK APPLIED IN DEMO MODE:\n"
            + feedback
        )

        return result, "demo"