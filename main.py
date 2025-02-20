from typing import List
from fastapi import FastAPI
from sqlalchemy.future import select
import models
import schemas
from database import engine, session

app = FastAPI()

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.on_event('shutdown')
async def shutdown():
    await session.close()
    await engine.dispose()

@app.post('/recipes/', response_model=schemas.RecipeCreate)
async def recipes(recipe: schemas.RecipeCreate) -> models.Recipe:
    new_recipe = models.Recipe(**recipe.dict())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe


@app.get('/recipes/', response_model=List[schemas.Recipes])
async def recipes() -> List[models.Recipe]:
    res = await session.execute(select(models.Recipe).order_by(models.Recipe.count_views.desc(), models.Recipe.cooking_time))
    return res.scalars().all()

@app.get('/recipes/{recipe_id}', response_model=schemas.RecipeDetail)
async def recipe_detail(recipe_id: int) -> models.Recipe:
    query = select(models.Recipe).where(models.Recipe.id == recipe_id)
    res = await session.execute(query)
    recipe = res.scalars().first()
    recipe.count_views += 1
    await session.commit()
    return recipe


# GET /recipes — получить список всех рецептов;
# GET /recipes/{recipe_id} — получить детальную информацию о конкретном рецепте;
# POST /recipes — создать новый рецепт.