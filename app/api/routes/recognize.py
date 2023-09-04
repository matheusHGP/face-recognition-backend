from fastapi import APIRouter, UploadFile

from app.core.services.recognize import RecognizeService

router = APIRouter(
    prefix="/recognize",
    tags=["recognize"],
)


@router.post("")
async def recognize(image: UploadFile):
    names = await RecognizeService().recognize(image)

    return {"names": names}
