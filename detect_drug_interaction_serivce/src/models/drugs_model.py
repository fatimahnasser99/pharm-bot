from pydantic import BaseModel
from typing import List, Optional

# class Drug(BaseModel):
#     name: str

class DrugInteractionOutput(BaseModel):
    found_interactions: bool = False
    interaction_type: Optional[str] = None
    interaction_description: Optional[str] = None
