from fastapi import APIRouter, status, HTTPException
from fastapi.params import Body
from fastapi.responses import Response

from typing import List, Optional

from app.database import database
from app.schema import Course, Courses, CoursesUpdate
from app.courses import courses
from datetime import date

router = APIRouter()


@router.get('/', response_model=List[Course])
async def courses_list():
    return await database.fetch_all(courses.select())


@router.get('/{course_id}', response_model=Course)
async def get_course(course_id: int):
    return await database.fetch_one(
        courses.select().where(courses.c.id == course_id)
    )


@router.post('/', status_code=201, summary='Create new course', response_description='Id of created course')
async def create_course(_course: Courses = Body(...,
                                                example={
                                                    "name": "Yalantis school",
                                                    "start_date": "2021-05-15",
                                                    "end_date": "2021-06-25",
                                                    'lectures': 12
                                                })):
    insert_id = await database.execute(
        courses.insert().values(
            name=_course.name,
            start_date=_course.start_date,
            end_date=_course.end_date,
            lectures=_course.lectures
        )
    )
    return insert_id


@router.put('/{course_id}', response_model=Course, summary='Update course',
            response_description='Updated course record by id', description='Update course if exists. Else getting error 404')
async def update_course(course_id: int, course: CoursesUpdate):
    if not await database.execute(
        courses.update().where(courses.c.id == course_id).values(
            **course.dict(exclude_unset=True)
        )
    ):
        raise HTTPException(status_code=404, detail='Course does\'nt exists')
    return await database.fetch_one(courses.select().where(courses.c.id == course_id))


@router.delete('/{course_id}', status_code=status.HTTP_204_NO_CONTENT, summary='Delete the course',
               response_description='No response', description='Delete the course by id')
async def delete_course(course_id: int):
    await database.execute(
        courses.delete().where(courses.c.id == course_id)
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get('/_search/', summary='Search courses',
            response_description='List of courses', )
async def search(
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        name: Optional[str] = None,
        lecture: Optional[int] = None):
    """
    ```
    :param start_date: '2021-05-15'
    :param end_date: '2021-05-12'
    :param name: Yal
    :param lecture: 15
    :return: List of courses
    ```
    **Example of use**
    ```
    import aiohttp

    base_url = ...

    async def fetch():
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params={"start_date":'2021-05-15',
            "end_date": '2021-05-12', "name": Yal, "lecture": 15}) as response:
                return await response.json()
    ```
    """
    query = courses.select()
    if start_date is not None:
        query = query.where(courses.c.start_date >= start_date)
    if end_date is not None:
        query = query.where(courses.c.end_date <= end_date)
    if name is not None:
        query = query.where(courses.c.name.ilike(f'%{name}%'))
    if lecture is not None:
        query = query.where(courses.c.lectures == lecture)

    return await database.fetch_all(query)
