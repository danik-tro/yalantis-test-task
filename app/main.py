from typing import List, Dict
from .schema import Course, Courses
from .courses import courses

from fastapi import FastAPI
from starlette.responses import RedirectResponse


from .routes import courses_route
from .database import database


tags_metadata = [
    {
        "name": "courses",
        "description": "Operations with courses. See more in docs.",
    }
]


app = FastAPI(description="""Yalantis test task""",
              title='Yalantis courses',
              openapi_tags=tags_metadata)
app.include_router(courses_route.router, prefix='/courses', tags=['courses'])


@app.get('/', tags=['courses'], description='Redirect to docs url')
async def index():
    return RedirectResponse(url='/docs/')


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


