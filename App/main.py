
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from App.settings  import setting


app= FastAPI()

template =Jinja2Templates("templates")

app.mount('/static',StaticFiles(directory="static"),'static')



@app.get("/")
def helth(request:Request):
    return template.TemplateResponse('index.html',{'request':request})







