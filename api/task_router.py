from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models import PredictingTaskType
from service import predict_task
router = APIRouter()

@router.post('/predict-type-task', tags=["Predict Task Type"])
async def predict_task(
    data: PredictingTaskType
):

    prompt = predict_task.build_prompt.run(data.task, data.main_type)

    return JSONResponse({'data': prompt})


@router.get('/', tags=["main"])
async def root():

    return JSONResponse({'data': "hello bang soal!"})
