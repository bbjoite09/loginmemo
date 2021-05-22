import hashlib

from tests.conftest import db


def test_로그인(client):
    id = "test05"
    pw = "test05"

    data = {
        'id': id,
        'pw': pw,
    }

def test_회원가입(client):
    data = {
        'id_give' : "test05",
        'pw_give': "test05"
    }

    response = client.post(
        '/api/reqisor',
        data=data
    )

    assert response, status_code == 200

    user = db.users.find_one({'id' : "test05"}, {'_id' : False})

    assert user['pw'] != 'test'
    hashlib.sha256('test'.encode()).hexdigest()