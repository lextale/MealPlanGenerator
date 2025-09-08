from pydantic import BaseModel, Field
from typing import List


class Macros(BaseModel):
    protein: float
    carbs: float
    fat: float


class Meal(BaseModel):
    mealName: str
    ingredients: List[str]
    instructions: str = Field(..., min_length=200, max_length=300)
    cookingTime: float
    calories: float
    macros: Macros
