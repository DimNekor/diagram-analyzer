from typing import List, Optional
from pydantic import BaseModel

from backend.models.step import Step

class Describing(BaseModel):
    status: str
    diagram_type: str
    steps: List[Step]
    processing_time_ms: int