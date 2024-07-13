from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.task_router import router as task_router
from mangum import Mangum
import os
from dotenv import load_dotenv

load_dotenv()

def handler(event, context):
   pass

app = FastAPI()
handler = Mangum(app) 

app.include_router(task_router)
