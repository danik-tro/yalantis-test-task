from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class Courses(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    lectures: int = Field(..., gt=0, description='The lectures must be greater than zero.')


class CoursesUpdate(Courses):
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    lectures: Optional[int] = None


class Course(Courses):
    id: int
    name: str
    start_date: datetime
    end_date: datetime
    lectures: int
