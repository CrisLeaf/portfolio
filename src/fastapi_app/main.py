from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import home, projects, contact, blog

import uvicorn

app = FastAPI()

# Montar archivos estáticos si los tienes (CSS, imágenes, etc.)
app.mount('/static', StaticFiles(directory='static'), name='static')

# Incluir routers
app.include_router(home.router)
app.include_router(projects.router)
app.include_router(contact.router)
app.include_router(blog.router)

@app.get('/')
def read_root():
    return {'Welcome': 'Bienvenido'}

if __name__ == '__main__':    
    uvicorn.run(app, port=8000)
    