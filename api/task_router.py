from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse

from models import *
from service.predict_task import build_prompt
from service.call_env import env_data
from service.paraphrase_question import paraphrase_question
from service.create_question import create_question
from service.create_answer import create_answer
from service.create_question_isian import create_question_isian
from service.create_material import create_material
from service.create_question_true_false import create_question_true_false
from service.create_question_mult_answer import create_question_mult_answer
from service.create_answer_isian import create_answer_isian
from service.create_answer_mult_answer import create_answer_mult_answer
from service.create_answer_tf import create_answer_tf
from service.extract_text import ExtractTextFromImage as ExtractText
router = APIRouter()

@router.post('/predict-type-task', tags=["Predict Task Type"])
async def predict_task_api(
    data: PredictingTaskType,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        if data.main_type == 'undecided' : 
            response_type = build_prompt.predict_type(data.question)
            response = build_prompt.run(data.question, response_type['type'])
            response = {
                'type' : response_type['type'],
                'subtype' : response,
                'description' : response_type['description']
            }
        else :
            if build_prompt.check_type(data.main_type) == True:
                response = build_prompt.run(data.question, data.main_type)
            else :
                return JSONResponse({'data': "Type denied"})


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
    return JSONResponse({'data': "check api create-question"})

@router.post('/create-question-isian', tags=["Create Question Isian"])
async def create_question_isian_api(
    data: CreateQuestionIsian,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = create_question_isian.run(data.question, data.explanation, data.answer)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/create-question-isian', tags=["Create Question Isian"])
async def create_question_isian_api():
    return JSONResponse({'data': "check api create-question-isian"})

@router.post('/create-question-tf', tags=["Create Question True False"])
async def create_question_tf_api(
    data: CreateQuestionTrueFalse,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = create_question_true_false.run(data.question, data.total_question)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/create-question-tf', tags=["Create Question True False"])
async def create_question_tf_api():
    return JSONResponse({'data': "check api create-question-tf"})

@router.post('/create-question-mult', tags=["Create Question Multiple Answer"])
async def create_question_tf_api(
    data: CreateQuestionMultAnswer,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = create_question_mult_answer.run(data.question)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/create-question-mult', tags=["Create Question Multiple Answer"])
async def create_question_tf_api():
    return JSONResponse({'data': "check api create-question-tf"})

@router.post('/create-answer', tags=["Create Answer"])
async def create_answer_api(
    data: CreateAnswer,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = create_answer.run(data.question, data.choice)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/create-answer', tags=["Create Answer"])
async def create_answer_api():
    return JSONResponse({'data': "check api create-answer"})

@router.post('/create-answer-isian', tags=["Create Answer Isian"])
async def create_answer_isian_api(
    data: CreateAnswerIsian ,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = create_answer_isian.run(data.question, data.answer, data.description)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/create-answer-isian', tags=["Create Answer Isian"])
async def create_answer_isian_api():
    return JSONResponse({'data': "check api create-answer"})

@router.post('/create-answer-mult-answer', tags=["Create Answer Multiple Answer"])
async def crea_answer_mult_answer(
    data: CreateAnswerMultAnswer ,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = create_answer_mult_answer.run(data.question, data.choice, data.answer, data.description)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/create-answer-mult-answer', tags=["Create Answer Multiple Answer"])
async def crea_answer_mult_answer():
    return JSONResponse({'data': "check api create-answer"})

@router.post('/create-answer-tf', tags=["Create Answer True/False"])
async def create_answer_tf_api(
    data: CreateAnswerTF ,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = create_answer_tf.run(data.question, data.choice, data.description)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/create-answer-tf', tags=["Create Answer True/False"])
async def create_answer_tf_api():
    return JSONResponse({'data': "check api create-answer"})

@router.post('/create-material', tags=["Create Material"])
async def create_material_api(
    data: CreateMaterial,  access_key: str = Header(None)
):
    if access_key == env_data.access_key() : 
        response = create_material.run(data.topic)

        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/create-material', tags=["Create Material"])
async def create_material_api():
    return JSONResponse({'data': "check api create-answer"})


@router.post('/extract-text', tags=["Extract Text"])
async def extract_text_api(
    data: ExtractTextFromImage, access_key: str = Header(None)
):
    print(access_key)
    if access_key == env_data.access_key() : 
        response = ExtractText.extract_text(data.image_url)
        return JSONResponse({'data': response})
    else : 
        return JSONResponse({'data': "wrong access key. access denied"})

@router.get('/', tags=["main"])
async def root():
    return JSONResponse({'data': "hello bang soal updated!"})
