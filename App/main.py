
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .routes.authRoute import router as authrouter
from .routes.DoctorRoute import router as doctorrouter


app= FastAPI()

template =Jinja2Templates("templates")

app.mount('/static',StaticFiles(directory="static"),'static')

app.include_router(authrouter, prefix="/auth")
app.include_router(doctorrouter, prefix="/doctor")


@app.get("/")
def helth(request:Request):
    return template.TemplateResponse('index.html',{'request':request})







