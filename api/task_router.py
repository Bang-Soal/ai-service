from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models import PredictingTaskType
from service.predict_task import build_prompt
from service.call_env import env_data
router = APIRouter()

@router.post('/predict-type-task', tags=["Predict Task Type"])
async def predict_task_api(
    data: PredictingTaskType
):
    print(env_data.access_key)
    if data.access_key == env_data.access_key() : 
        prompt = build_prompt.run(data.question, data.main_type)

        return JSONResponse({'data': prompt})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/predict-type-task', tags=["Predict Task Type"])
async def predict_task_api():


    return JSONResponse({'data': "check api predict-task-type"})


@router.get('/test', tags=["test aja"])
async def predict_task_api():


    return JSONResponse({'data': "test 2"})



@router.get('/', tags=["main"])
async def root():

    return JSONResponse({'data': "hello bang soal updated!"})
