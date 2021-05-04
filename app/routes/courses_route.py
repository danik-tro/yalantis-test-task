from fastapi import APIRouter, status, HTTPException
from fastapi.responses import Response

from typing import List, Optional

from app.database import database
from app.schema import Course, Courses, CoursesUpdate
from app.courses import courses
from datetime import datetime

router = APIRouter()


@router.get('/', response_model=List[Course])
async def courses_list():
    return await database.fetch_all(courses.select())


@router.get('/{course_id}', response_model=Course)
async def get_course(course_id: int):
    return await database.fetch_one(
        courses.select().where(courses.c.id == course_id)
    )


@router.post('/', status_code=201)
async def create_course(_course: Courses):
    insert_id = await database.execute(
        courses.insert().values(
            name=_course.name,
            start_date=_course.start_date,
            end_date=_course.end_date,
            lectures=_course.lectures
        )
    )
    return insert_id


@router.put('/{course_id}', response_model=Course)
async def update_course(course_id: int, course: CoursesUpdate):
    if not await database.execute(
        courses.update().where(courses.c.id == course_id).values(
            **course.dict(exclude_unset=True)
        )
    ):
        raise HTTPException(status_code=404, detail='Course does\'nt exists')
    return await database.fetch_one(courses.select().where(courses.c.id == course_id))


@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: int):
    await database.execute(
        courses.delete().where(courses.c.id == course_id)
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/_search/')
async def search(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        name: Optional[str] = None,
        lecture: Optional[int] = None):
    query = courses.select()
    if start_date is not None:
        query = query.where(courses.c.start_date >= start_date)
    if end_date is not None:
        query = query.where(courses.c.end_date <= end_date)
    if name is not None:
        query = query.where(courses.c.name.ilike(f'%{name}%'))
    if lecture is not None:
        query = query.where(courses.c.lecture == lecture)

    return await database.fetch_all(query)
