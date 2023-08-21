from pydantic import BaseModel, HttpUrl

from typing import Sequence


class Recipe(BaseModel):
    id: int
    label: str
    source: str

    # Pydantic HttpUrl helper. This will enforce expected URL
    # components, such as the presence of a scheme(http/https)
    url: HttpUrl

# Uses Pydantic’s recursive capability to define a field that
#  refers to another Pydantic class we’ve previously defined,
#  the Recipe class. We specify that the results field will
#  be a Sequence (which is an iterable with support for
#  len and __getitem__) of Recipes.
class RecipeSearchResults(BaseModel):
    results: Sequence[Recipe]


class RecipeCreate(BaseModel):
    label: str
    source: str
    url: HttpUrl
    submitter_id: int
