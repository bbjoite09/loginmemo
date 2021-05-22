import os

import jwt
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify

bp = Blueprint(
    'user', # 블루프린트 이름
    __name__,   # 파일 등록(현재파일)
    url_prefix='/user' # 패스 접두사
)
load_dotenv()
# load_dotenv() 설정
JWT_SECRET = os.environ['JWT_SECRET']

@bp.route('/user', methods=['POST'])
def user_info():
    token_receive = request.headers['authorization']
    token = token_receive.split()[1]
    print(token)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        id = payload['id']
        return jsonify({'result': 'success', 'id': id})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})