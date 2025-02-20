from pydantic import BaseModel


class BaseRecipe(BaseModel):
    title: str

class Recipes(BaseRecipe):
    count_views: int
    cooking_time: int


class RecipeCreate(BaseRecipe):
    count_views: int
    cooking_time: int
    description: str
    ingredients: list[str]

    class Config:
        from_attributes = True


class RecipeDetail(BaseRecipe):
    id: int
    count_views: int
    cooking_time: int
    description: str
    ingredients: list[str]


