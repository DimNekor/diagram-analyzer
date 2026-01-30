from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from PIL import Image
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI(title="Diagram Recognition API", version="0.1")

class Step(BaseModel):
    step: int
    action: str
    actor: Optional[str] = None
    system: Optional[str] = None

class DescribeResponse(BaseModel):
    status: str
    diagram_type: str
    steps: List[Step]
    processing_time_ms: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/v1/process", response_model=DescribeResponse)
async def describe_diagram(
    image: UploadFile = File(...),
    language: str = Form("ru"),
    diagram_type_hint: str = Form("auto"),
):
    t0 = time.time()

    if image.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(status_code=400, detail="Unsupported image type")

    demo_steps = [
        Step(step=1, action="Распознать элементы диаграммы", actor="System", system="VisionModel"),
        Step(step=2, action="Построить порядок выполнения шагов", actor="System", system="Parser"),
        Step(step=3, action="Сгенерировать текстовое описание", actor="System", system="LLM"),
    ]

    ms = int((time.time() - t0) * 1000)
    return DescribeResponse(
        status="success",
        diagram_type=diagram_type_hint.upper() if diagram_type_hint != "auto" else "Unknown",
        steps=demo_steps,
        processing_time_ms=ms,
    )