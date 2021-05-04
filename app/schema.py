from pydantic import BaseModel
from datetime import datetime


class Courses(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    lectures: int


class Course(Courses):
    id: int
