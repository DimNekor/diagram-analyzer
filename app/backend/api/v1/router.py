from fastapi import APIRouter

from backend.api.v1 import health, process

router = APIRouter(prefix="/v1")

router.include_router(health.router)
router.include_router(process.router)