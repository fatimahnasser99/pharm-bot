from pydantic import BaseModel
from typing import List

class QueryModel(BaseModel):
    drugs: List[str]
