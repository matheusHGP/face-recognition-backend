from typing import List, Annotated
from fastapi import APIRouter, UploadFile, Form

from app.core.services.train import TrainService

router = APIRouter(
    prefix="/train",
    tags=["train"],
)


@router.post("")
async def upload_train_images(
    name: Annotated[str, Form()],
    images: List[UploadFile]
):
    await TrainService().upload_images(name, images)

    return {"message": "upload realizado com sucesso"}
