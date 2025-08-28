from fastapi import APIRouter
from app.backend.services import model_service

router = APIRouter(prefix="/model")



@router.post(path="/invoke")
async def invoke(userinput : str):
    return await model_service.invoke(userinput=userinput)

