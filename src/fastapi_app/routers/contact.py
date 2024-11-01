from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/contact')
async def contact(request: Request):
    return templates.TemplateResponse('contact.html', {'request': request})

@router.post('/contact')
async def submit_contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    # Aquí procesas el formulario de contacto
    return {'message': 'Mensaje recibido!'}