from pydantic import BaseModel
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