from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import Form

class PredictingTaskType(BaseModel):
    question: Annotated[str, Form()]
    main_type: Annotated[str, Form()]

class ParaphraseQuestion(BaseModel):
    question: Annotated[str, Form()]
    choice: Annotated[str, Form()]
    content: Annotated[str, Form()]
    raw_answer: Annotated[str, Form()]

class CreateQuestion(BaseModel):
    question: Annotated[str, Form()]
    choice: Annotated[str, Form()]
    raw_answer: Annotated[str, Form()]

class CreateAnswer(BaseModel):
    question: Annotated[str, Form()]
    choice: Annotated[str, Form()]

class CreateAnswerIsian(BaseModel):
    question: Annotated[str, Form(), Field(default="Panitia jalan sehat akan membuat kupon bernomor yang terdiri atas 4 angka yang disusun oleh angkaangka \( 0,1,3,5 \) dan 7 . Jika angka pertama atau terakhir tidak 0 , maka banyak kupon yang dapat dibuat adalah ....")]
    answer: Annotated[str, Form(), Field(default="600")]
    description: Annotated[str, Form(), Field(default="Banyaknya kupon yang dapat dibuat adalah \( 5^{4}-5^{2}=625-25=600 \)")]


class CreateMaterial(BaseModel):
    topic: Annotated[str, Form()]

class CreateQuestionIsian(BaseModel):
    question: Annotated[str, Form()]
    explanation: Annotated[str, Form()]
    answer: Annotated[str, Form()]


class CreateQuestionTrueFalse(BaseModel):
    question: Annotated[str, Form()]
    total_question: Annotated[str, Form()]

class CreateQuestionMultAnswer(BaseModel):
    question: Annotated[str, Form()]