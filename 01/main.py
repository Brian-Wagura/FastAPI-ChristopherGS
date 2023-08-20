from fastapi import FastAPI, APIRouter

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

# Register the router we created on the FastAPI object.
app.include_router(api_router)

# Applies when a module is called directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
