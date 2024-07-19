from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from models import PredictingTaskType, ParaphraseQuestion, CreateQuestion
from service.predict_task import build_prompt
from service.call_env import env_data
from service.paraphrase_question import paraphrase_question
from service.create_question import create_question
router = APIRouter()

@router.post('/predict-type-task', tags=["Predict Task Type"])
async def predict_task_api(
    data: PredictingTaskType,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = build_prompt.run(data.question, data.main_type)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/predict-type-task', tags=["Predict Task Type"])
async def predict_task_api():
    return JSONResponse({'data': "check api predict-task-type"})

@router.post('/paraphrase-question', tags=["Paraphrase Question"])
async def paraphrase_question_api(
    data: ParaphraseQuestion,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = paraphrase_question.run(data.question, data.choice, data.content, data.raw_answer)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/paraphrase-question', tags=["Paraphrase Question"])
async def paraphrase_question_api():
    return JSONResponse({'data': "check api paraphrase-question"})

@router.post('/create-question', tags=["Create Question"])
async def create_question_api(
    data: CreateQuestion,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = create_question.run(data.question, data.choice, data.raw_answer)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/create-question', tags=["Create Question"])
async def create_question_api():
    return JSONResponse({'data': "check api paraphrase-question"})


@router.get('/', tags=["main"])
async def root():

    return JSONResponse({'data': "hello bang soal updated!"})
