from typing import List, Dict

from fastapi import FastAPI
from .schema import Course, Courses
from .database import database
from .courses import courses

app = FastAPI(description="""Yalantis test task""")


@app.get('/')
async def index():
    return {'message': ''}


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/courses/', response_model=Dict[str, List[Course]])
async def courses_list():
    return {"courses": await database.fetch_all(courses.select())}


@app.get('/courses/{course_id}', response_model=Courses)
async def get_course(course_id: int):
    return {"course": (await database.fetch_all(
        courses.select().where(courses.c.id == course_id)
    ))[0]}


@app.post('/courses/')
async def create_course(_course: Courses):
    insert_id = await database.execute(
        courses.insert().values(
            name=_course.name,
            start_date=_course.start_date,
            end_date=_course.end_date,
            lectures=_course.lectures
        )
    )
    return {'course': {'created': insert_id}}


@app.put('/courses/{course_id}')
async def update_course(course_id: int):
    return {'message': 'updated course'}


@app.delete('/courses/{course_id}')
async def delete_course(course_id: int):
    await database.execute(
        courses.delete().where(courses.c.id == course_id)
    )
    return {'course': {'deleted': course_id}}


@app.get('/search/')
async def search(start_date, end_date, name, lecture):
    return {'message': 'searches courses'}
