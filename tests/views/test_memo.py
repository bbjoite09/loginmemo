import datetime

import jwt

from tests.conftest import db

def test_메모장_저장(client):
    # 실제 네이버 서버를 호출하지 않는 mocing
    url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=101&oid=014&aid=0004643220'
    comment = "tests comment"

    data = {
        'url_give': url,
        'comment_give': comment,
    }
    # 임의의ㅡ 사용자 JWT 만들기
    expiration_time = datetime.timedelta(hours=1)
    payload = {
        'id': 'tester',
        # JWT 유효 기간 - 이 시간 이후에는 JWT 인증이 불가능합니다.
        'exp': datetime.datetime.utcnow() + expiration_time,
    }
    # .env 설정과 맞게 jwt 시크릿 설정
    token = jwt.encode(payload, 'secret')
    headers = {
        'authorization' : f'Bearer {token}'
    }

    response = client.post(
        '/memo',
        data=data,
        headers=headers
    )

    assert response.status_code == 200

    # mongoDB에 저장되었는지 확인

    memo = db.articles.find_one(
        {'id' : 'tester'}, {'_id' : False}
    )
    assert memo['comment'] == comment