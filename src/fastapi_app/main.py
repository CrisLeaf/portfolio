from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.wsgi import WSGIMiddleware
from routers import home, projects, contact, blog

import uvicorn

import sys
sys.path.append('../dash_app/')

from home_plot import create_start_dash_app


app = FastAPI()

# Montar archivos estáticos si los tienes (CSS, imágenes, etc.)
app.mount('/static', StaticFiles(directory='static'), name='static')

# Incluir routers
app.include_router(home.router)
app.include_router(projects.router)
app.include_router(contact.router)
app.include_router(blog.router)


home_plot = create_start_dash_app(requests_pathname_prefix="/home_plot/")
app.mount("/home_plot", WSGIMiddleware(home_plot.server))


@app.get('/')
def read_root():
    return {'Welcome': 'Bienvenido'}

if __name__ == '__main__':    
    uvicorn.run(app, port=8000)
