# Yalantis Test Task 
>Trotsenko Daniil

## 1. Descriptions of the task
### 1.1 Create a series of endpoints for the following functions:

* Adding a course to the catalog
* Display a list of courses
* Display course details by id (detailed course page should display full course information)
* Search for a course by title and filter by date
* Change course attributes
* Delete course


### 1.2 The course must have the following attributes:
* Name
* Start date
* End date
* Number of lectures

## 2. Solving the task
### 2.1 Structure of the project

```
├── app
│   ├── courses.py
│   ├── database.py
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routes
│   │   ├── courses_route.py
│   │   └── __init__.py
│   ├── schema.py
│   └── test
│       ├── __init__.py
│       └── test_app.py
├── Dockerfile
├── Pipfile
├── requirements.txt
└── set_up.py
```
### 2.2 Routers
````
GET /courses/ - Courses List
POST /courses/ - Create Course
GET /courses/{course_id} - Get Course
PUT /courses/{course_id} - Update Course
DELETE /courses/{course_id} - Delete Course
GET /courses/_search/ - Search courses
GET /docs - Documentation
````
See more in docs by router **/docs**

### 2.3 Run project
#### 2.3.1 Build and start docker container
````
$ git clone https://github.com/danik-tro/yalantis-test-task.git
$ cd yalantis-test-task
$ docker build . -t danik-tro/yalantis-task
$ docker run -p 8000:80 danik-tro/yalantis-task
````
The project will be available at the address **http://localhost:8000**
#### 2.3.2 Run project without docker container(Linux)
````
$ git clone https://github.com/danik-tro/yalantis-test-task.git
$ cd yalantis-test-task
$ python -m venv env
$ source env/bin/activate
$ pip install --no-cache-dir -r requirements.txt
$ python set_up.py
$ python -m pytest app/test/
$ uvicorn app.main:app --port 8000
> INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
````
