from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from .routes.authRoute import router as authrouter
from .routes.dashbordRoute import router as dashrouter
from .routes.doctorRoute import router as doctorrouter
from .routes.patientRoute import router as patientrouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError 





_version_ ="0.1.0"

app= FastAPI(version=_version_,description=" ")

template =Jinja2Templates("templates")

app.mount('/static',StaticFiles(directory="static"),'static')

app.include_router(dashrouter,prefix='/dashbord',tags=['dashboard'])
app.include_router(authrouter, prefix="/auth",tags=['auth'])
app.include_router(doctorrouter, prefix="/doctor",tags=['doctor'])
app.include_router(patientrouter, prefix="/patient",tags=['patient'])





@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]
    message = first_error["msg"]
    return JSONResponse(status_code=422, content={'detail':f"{field}: {message}"})

@app.get("/",response_class=HTMLResponse)
def helth(request:Request):
    return template.TemplateResponse('index.html',{'request':request})


@app.get('/auth/login',response_class=HTMLResponse)
def serve_login_page(request:Request):
    return template.TemplateResponse("login.html",{'request':request})

@app.get('/admin',response_class=HTMLResponse)
def serve_login_page(request:Request):
    return template.TemplateResponse("admin.html",{'request':request})

@app.get('/doctor',response_class=HTMLResponse)
def serve_login_page(request:Request):
    return template.TemplateResponse("doctor.html",{'request':request})

@app.get('/patient',response_class=HTMLResponse)
def serve_login_page(request:Request):
    return template.TemplateResponse("patient.html",{'request':request})




