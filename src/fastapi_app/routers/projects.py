from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory='templates')

@router.get('/projects')
async def projects(request: Request):
    sample_projects = [
        {'name': 'Project 1', 'description': 'Descripción del Proyecto 1'},
        {'name': 'Project 2', 'description': 'Descripción del Proyecto 2'},
    ]
    return templates.TemplateResponse('projects.html', {'request': request, 'projects': sample_projects})