from pydantic import BaseModel
from typing import List, Optional

# class Drug(BaseModel):
#     name: str

class DrugExtractionOutput(BaseModel):
    drugs_list: Optional[List[str]] = []
