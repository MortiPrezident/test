import pytest
from fastapi.testclient import TestClient
from main import app
from models import Recipe

client = TestClient(app)


@pytest.fixture
def new_recipe_data():
    return {
        "title": "Test Recipe",
        "count_views": 11,
        "cooking_time": 30,
        "description": "A delicious test recipe.",
        "ingredients": ["ingredient1", "ingredient2"]
    }


@pytest.fixture
def mock_recipe():
    return Recipe(
        id=1,
        title="Test Recipe",
        count_views=11,
        cooking_time=30,
        description="A delicious test recipe.",
        ingredients=["ingredient1", "ingredient2"]
    )


def test_create_recipe(new_recipe_data):
    response = client.post("/recipes/", json=new_recipe_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == new_recipe_data["title"]
    assert data["count_views"] == new_recipe_data["count_views"]
    assert data["cooking_time"] == new_recipe_data["cooking_time"]
    assert data["description"] == new_recipe_data["description"]
    assert data["ingredients"] == new_recipe_data["ingredients"]


def test_get_recipes(mock_recipe):

    response = client.get("/recipes/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data)
    assert data[0]["title"] == mock_recipe.title
    assert data[0]["count_views"] == mock_recipe.count_views
    assert data[0]["cooking_time"] == mock_recipe.cooking_time


def test_get_recipe_detail(mock_recipe):
    response = client.get(f"/recipes/{mock_recipe.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mock_recipe.id
    assert data["title"] == mock_recipe.title
    assert data["count_views"] == mock_recipe.count_views + 1
    assert data["cooking_time"] == mock_recipe.cooking_time
    assert data["description"] == mock_recipe.description
    assert data["ingredients"] == mock_recipe.ingredients
