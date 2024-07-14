from pydantic import BaseModel
from typing import Annotated
from fastapi import Form

class PredictingTaskType(BaseModel):
    question: Annotated[str, Form()]
    main_type: Annotated[str, Form()]