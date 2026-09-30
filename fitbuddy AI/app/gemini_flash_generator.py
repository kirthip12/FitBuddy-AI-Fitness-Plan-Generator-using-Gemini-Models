from __future__ import annotations

import os

from .gemini_client import generate_text


TIP_MODEL = os.getenv(
    "GEMINI_TIP_MODEL",
    "gemini-3.8-flash"
)


def generate_nutrition_tip_with_flash(
    goal: str
):

    prompt = f"""
You are FitBuddy.

Give one useful nutrition or recovery tip for someone
whose fitness goal is:

{goal}

Requirements:

- 3 to 5 sentences.
- Give practical advice.
- Encourage balanced food.
- Mention hydration or recovery where useful.
- Do not recommend extreme dieting.
- Do not prescribe supplements.
- Do not give medical treatment advice.
"""

    try:

        result = generate_text(
            prompt,
            TIP_MODEL
        )

        return result, "gemini"

    except Exception:

        tips = {

            "weight loss":
            """
Focus on balanced meals containing vegetables,
a suitable protein source, whole-food carbohydrates,
and water. Avoid crash diets and focus on consistent,
sustainable habits. Good sleep and regular activity
also support healthy progress.
""",

            "muscle gain":
            """
Include a protein source in your main meals such as
eggs, dairy, fish, chicken, soy, beans, or lentils.
Combine protein with carbohydrates and vegetables to
support training and recovery. Stay hydrated and
prioritize adequate sleep.
""",

            "general wellness":
            """
Try to build balanced meals using vegetables or fruit,
protein, whole grains, and healthy fats. Drink water
regularly throughout the day. Consistent sleep and
regular physical activity are also important.
""",

            "flexibility":
            """
Stay hydrated and include a variety of vegetables,
fruit, protein, and whole-food carbohydrates. Use gentle
mobility exercises regularly rather than forcing stretches.
Adequate sleep helps your body recover.
"""
        }

        return (
            tips.get(
                goal,
                tips["general wellness"]
            ).strip(),
            "demo"
        )