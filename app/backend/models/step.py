from pydantic import BaseModel
from typing import List, Optional

class Step(BaseModel):
    step: int
    action: str
    actor: Optional[str] = None
    system: Optional[str] = None