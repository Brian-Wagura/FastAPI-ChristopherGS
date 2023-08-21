from fastapi import FastAPI, APIRouter, Query, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Any
from schemas import RecipeSearchResults, Recipe, RecipeCreate
from recipe_data import RECIPES

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

# Instantiate a FastAPI app object, which is a
# Python class that provides all the functionality for
# your API.
app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

# Instantiate an APIRouter which is how we
#  can group our API endpoints
api_router = APIRouter()


# Define a basic GET endpoint for our API.
@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """

    # Updated to serve a Jinja2 template
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": RECIPES},
    )


# Include a response_model field. Here we define the structure of the JSON
# response, and we do this via Pydantic.
@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
# The type hints for the function arguments which match
#  the URL path parameters are used by FastAPI to perform
#  automatic validation and conversion.
def fetch_recipe(*, recipe_id: int) -> Any:
    """
    Fetch a single recipe by id
    """
    # Simulate fetching data by ID from a database with
    # a simple list comprehension with an ID conditional check.
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )
    return result[0]


@api_router.get("/search/", status_code=200, response_model=Recipe)
# Its arguments represent the query parameters to the endpoint.
#  There are two arguments: keyword and max_results.
#  Query class, which allows us add additional validation and
#  requirements to our query params.
def search_recipes(
    *,
    keyword: str | None = Query(None, min_length=3, example="burger"),
    max_results: int | None = 10,
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        return {"results": RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:max_results]}


@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate) -> dict:
    """
    Create a new recipe in memory
    """

    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
    )
    RECIPES.append(recipe_entry.model_dump())

    return recipe_entry


# Register the router we created on the FastAPI object.
app.include_router(api_router)

# Applies when a module is called directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8180, log_level="debug")
