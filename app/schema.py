from typing import Optional

from pydantic import BaseModel, Field
from datetime import date


class Courses(BaseModel):
    name: str
    start_date: date
    end_date: date
    lectures: int = Field(..., gt=0, description='The lectures must be greater than zero.')


class CoursesUpdate(Courses):
    name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    lectures: int = Field(None, gt=0, description='The lectures must be greater than zero.')


class Course(Courses):
    id: int
    name: str
    start_date: date
    end_date: date
    lectures: int = Field(..., gt=0, description='The lectures must be greater than zero.')
