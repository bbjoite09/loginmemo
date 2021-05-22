import datetime
import hashlib
import os

import jwt
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from app import db

load_dotenv()
# load_dotenv() 설정
JWT_SECRET = os.environ['JWT_SECRET']

bp = Blueprint(
    'api', # 블루프린트 이름
    __name__,   # 파일 등록(현재파일)
    url_prefix='/api' # 패스 접두사
)

# 가입 API
@bp.route('/api/register', methods=['POST'])
def api_register():
    id = request.form['id_give']
    pw = request.form['pw_give']

    pw_hash = hashlib.sha256(pw.encode()).hexdigest()
    db.user.insert_one({'id': id, 'pw': pw_hash})

    return jsonify({'result': 'success'})


# 네이버 가입 API
@bp.route('/api/register/naver', methods=['POST'])
def api_register_naver():
    naver_id = request.form['naver_id_give']
    print(naver_id)

    # 아직 가입하지 않은 naver id 케이스에서는 가입까지 처리
    if not db.user.find_one({'id': naver_id}, {'_id': False}):
        db.user.insert_one({'id': naver_id, 'pw': ''})

    expiration_time = datetime.timedelta(hours=1)
    payload = {
        'id': naver_id,
        # JWT 유효 기간 - 이 시간 이후에는 JWT 인증이 불가능합니다.
        'exp': datetime.datetime.utcnow() + expiration_time,
    }
    token = jwt.encode(payload, JWT_SECRET)

    return jsonify({'result': 'success', 'token': token})


# 로그인 API
@bp.route('/api/login', methods=['POST'])
def api_login():
    id = request.form['id_give']
    pw = request.form['pw_give']

    pw_hash = hashlib.sha256(pw.encode()).hexdigest()
    user = db.user.find_one({'id': id, 'pw': pw_hash})

    # 로그인 성공 시 JWT 리턴
    if user:
        expiration_time = datetime.timedelta(hours=1)
        payload = {
            'id': id,
            # JWT 유효 기간 - 이 시간 이후에는 JWT 인증이 불가능합니다.
            'exp': datetime.datetime.utcnow() + expiration_time,
        }
        token = jwt.encode(payload, JWT_SECRET)
        return jsonify({'result': 'success', 'token': token})

    return jsonify({'result': 'fail', 'msg': '아이디 비밀번호 불일치'})