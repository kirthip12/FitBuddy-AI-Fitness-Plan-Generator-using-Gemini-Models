from __future__ import annotations

import os

from .gemini_client import generate_text


WORKOUT_MODEL = os.getenv(
    "GEMINI_WORKOUT_MODEL",
    "gemini-3.8-flash"
)


def demo_plan(
    name: str,
    goal: str,
    intensity: str,
    experience_level: str
) -> str:

    return f"""
FITBUDDY - 7 DAY WORKOUT PLAN

User:
{name}

Goal:
{goal}

Intensity:
{intensity}

Experience:
{experience_level}


DAY 1 - FULL BODY

Warm-up:
5-10 minutes of walking and mobility.

Exercises:
Squats - 3 x 10
Incline Push-ups - 3 x 8
Glute Bridges - 3 x 12
Bodyweight Rows - 3 x 10

Cooldown:
5 minutes of easy walking and stretching.


DAY 2 - CARDIO + CORE

Warm-up:
5-10 minutes easy movement.

Cardio:
20-30 minutes brisk walking or cycling.

Core:
Dead Bug - 3 x 10 each side
Plank - 3 x 20-30 seconds

Cooldown:
5 minutes.


DAY 3 - RECOVERY

Easy walking:
20-30 minutes.

Mobility:
10 minutes gentle mobility exercises.

Focus on recovery.


DAY 4 - UPPER BODY

Warm-up:
5-10 minutes.

Exercises:
Push-ups - 3 x 8
Rows - 3 x 10
Shoulder Press - 3 x 10
Bird Dog - 3 x 10 each side

Cooldown:
5-10 minutes.


DAY 5 - LOWER BODY

Warm-up:
5-10 minutes.

Exercises:
Squats - 3 x 10
Reverse Lunges - 3 x 8 each side
Hip Hinges - 3 x 10
Calf Raises - 3 x 15

Cooldown:
5 minutes.


DAY 6 - CARDIO + MOBILITY

Warm-up:
5 minutes.

Cardio:
25-35 minutes.

Mobility:
10 minutes.

Cooldown:
5 minutes.


DAY 7 - REST

Take a rest day.

Optional:
Easy walking and gentle stretching.


GENERAL GUIDELINES

Rest 60-120 seconds between strength sets.

Increase exercise difficulty gradually.

Stay hydrated.

Get adequate sleep.

SAFETY:

This is a general wellness plan and not medical advice.
Stop exercising if you experience unusual pain,
dizziness, chest pain, or severe breathing difficulty.
"""


def generate_workout_gemini(
    name: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    experience_level: str
):

    prompt = f"""
You are FitBuddy, an AI fitness planning assistant.

Create a safe and practical 7-day general fitness plan.

USER INFORMATION

Name: {name}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}
Experience level: {experience_level}


REQUIREMENTS

1. Create exactly 7 days.
2. Give each day a clear title.
3. Include warm-up.
4. Include exercises.
5. Include sets/repetitions or duration.
6. Include rest guidance.
7. Include cooldown.
8. Include recovery guidance.
9. Respect the selected experience level.
10. Respect the selected intensity.
11. Do not diagnose diseases.
12. Do not prescribe medicines.
13. Do not recommend extreme diets.
14. Include a short safety note.

Use simple readable formatting.

Return only the workout plan.
"""

    try:

        result = generate_text(
            prompt,
            WORKOUT_MODEL
        )

        return result, "gemini"

    except Exception:

        return (
            demo_plan(
                name,
                goal,
                intensity,
                experience_level
            ),
            "demo"
        )