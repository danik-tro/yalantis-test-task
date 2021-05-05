from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_app():
    response = client.get('/courses/')
    assert response.status_code == 200
    assert isinstance(response.json(), list) is True
    assert len(response.json()) >= 0


def test_post_course():
    response = client.post('/courses/', json={
        "name": 'Test_1',
        "start_date": "2020-09-15",
        "end_date": "2021-09-15",
        "lectures": 5
    })

    assert response.status_code == 201
    assert isinstance(response.json(), int) is True

    response = client.delete(f'/courses/{response.json()}')

    assert response.status_code == 204


def test_full_crud():

    course = {
        "name": 'Test_1',
        "start_date": "2020-09-15",
        "end_date": "2021-09-15",
        "lectures": 5
    }

    response = client.post('/courses/', json=course)
    response_id = response.json()
    assert response.status_code == 201
    assert isinstance(response_id, int) is True

    response = client.get(f'/courses/{response_id}')

    assert response.status_code == 200
    assert response.json() == {
        "id": response_id,
        **course
    }

    update_name = {"name": "Test_2"}
    response = client.put(f'/courses/{response_id}', json={
        **update_name
    })

    assert response.status_code == 200
    assert response.json() == {"id": response_id, **course, **update_name}

    update_date = {"name": "Test_3",
                   "start_date": "2020-05-11",
                   "end_date": "2021-02-15",
                   }
    response = client.put(f'/courses/{response_id}', json={
        **update_date
    })

    assert response.status_code == 200
    assert response.json() == {"id": response_id, **course, **update_date}

    response = client.get('/courses/_search/', params={
        "start_date": "2019-05-11",
        "end_date": "2022-02-15",
        "name": "est",
        "lectures": 5
    })

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]['id'] == response_id

    response = client.delete(f'/courses/{response_id}')

    assert response.status_code == 204

    response = client.get(f'/courses/{response_id}')
    assert response.status_code == 200
    assert response.json() is None

