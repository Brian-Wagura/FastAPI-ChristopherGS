from fastapi import FastAPI, APIRouter

# Example recipe data in the RECIPE list of dictionaries.
RECIPES = [
    {
        "id": 1,
        "label": "Fried Chicken Burger",
        "source": "ArtCaffe",
        "url": "https://glovoapp.com/ke/en/nairobi/artcaffe/?content=burgers-c.1737394471",
    },
    {
        "id": 2,
        "label": "Texas Burger",
        "source": "ArtCaffe",
        "url": "https://glovoapp.com/ke/en/nairobi/artcaffe/?content=burgers-c.1737394471",
    },
    {
        "id": 3,
        "label": "Cheese Burger",
        "source": "ArtCaffe",
        "url": "https://glovoapp.com/ke/en/nairobi/artcaffe/?content=burgers-c.1737394471",
    },
]

# Instantiate a FastAPI app object, which is a
# Python class that provides all the functionality for
# your API.
app = FastAPI(title="Recipe API", openapi_url="/openapi.json")

# Instantiate an APIRouter which is how we
#  can group our API endpoints
api_router = APIRouter()


# Define a basic GET endpoint for our API.
@api_router.get("/", status_code=200)
def root() -> dict:
    """
    Root GET
    """

    return {"msg": "Hello World!"}


#  The curly braces indicate the parameter value,
#  which needs to match one of the arguments taken
#  by the endpoint function fetch_recipe.
@api_router.get("/recipe/{recipe_id}", status_code=200)
# The type hints for the function arguments which match
#  the URL path parameters are used by FastAPI to perform
#  automatic validation and conversion.
def fetch_recipe(*, recipe_id: int) -> dict:
    """
    Fetch a single recipe by id
    """
    # Simulate fetching data by ID from a database with
    # a simple list comprehension with an ID conditional check.
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if result:
        # Serialized JSON response.
        return result[0]


# Register the router we created on the FastAPI object.
app.include_router(api_router)

# Applies when a module is called directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
