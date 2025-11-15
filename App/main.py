from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .db.db import init_db
from .routes.authRoute import router as authrouter
from .routes.doctorRoute import router as doctorrouter
from .routes.patientRoute import router as patientrouter


from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):
    await init_db()
    print('App is running...')
    yield 
    print("shutdown...")
    

app= FastAPI(lifespan=lifespan)

template =Jinja2Templates("templates")

app.mount('/static',StaticFiles(directory="static"),'static')

app.include_router(authrouter, prefix="/auth",tags=['auth'])
app.include_router(doctorrouter, prefix="/doctor",tags=['doctor'])
app.include_router(patientrouter, prefix="/patient",tags=['patient'])


@app.get("/")
def helth(request:Request):
    return template.TemplateResponse('index.html',{'request':request})


@app.get('/auth/login')
def serve_login_page(request:Request):
    return template.TemplateResponse("login.html",{'request':request})

@app.get('/admin')
def serve_login_page(request:Request):
    return template.TemplateResponse("admin.html",{'request':request})

@app.get('/doctor')
def serve_login_page(request:Request):
    return template.TemplateResponse("doctor.html",{'request':request})

@app.get('/patient')
def serve_login_page(request:Request):
    return template.TemplateResponse("patient.html",{'request':request})




