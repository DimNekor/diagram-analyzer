import time
from fastapi import APIRouter, UploadFile, File, Form, HTTPException

from backend.models.step import Step
from backend.models.describing import Describing

router = APIRouter()

@router.post("/process", response_model=Describing)
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
    return Describing(
        status="success",
        diagram_type=diagram_type_hint.upper() if diagram_type_hint != "auto" else "Unknown",
        steps=demo_steps,
        processing_time_ms=ms,
    )