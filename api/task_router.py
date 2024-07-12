from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models import PredictingTaskType
from service.predict_task import build_prompt
router = APIRouter()

@router.post('/predict-type-task', tags=["Predict Task Type"])
async def predict_task_api(
    data: PredictingTaskType
):

    prompt = build_prompt.run(data.question, data.main_type)

    return JSONResponse({'data': prompt})


@router.get('/', tags=["main"])
async def root():

    return JSONResponse({'data': "hello bang soal updated!"})
