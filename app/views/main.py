import os

import jwt
from dotenv import load_dotenv
from flask import Blueprint, request, render_template

from app import db
load_dotenv()
# load_dotenv() 설정
JWT_SECRET = os.environ['JWT_SECRET']

bp = Blueprint(
    'main', # 블루프린트 이름
    __name__,   # 파일 등록(현재파일)
    url_prefix='/' # 패스 접두사
)

# API 추가
@bp.route('/', methods=['GET'])  # 데코레이터 문법
def index():  # 함수 이름은 고유해야 한다
    token = request.cookies.get('loginToken')

    if token:
        try:
            payload = jwt.dcode(token, JWT_SECRET, algorithms=['HS256'])
            id = payload['id']
            memos = list(db.articles.find({'id': id}, {'_id': False}))
        except jwt.ExpiredSignatureError:
            memos = []
    else:
        memos = []

    return render_template('index.html', test='테스트', memos=memos)

# 네아로 콜백
@bp.route('/naver', methods=['GET'])
def callback():
    CLIENT_ID = os.environ['CLIENT_ID']
    CALLBACK_URL = os.environ['CALLBACK_URL']

    return render_template('callback.html', CALLBACK_URL=CALLBACK_URL, CLIENT_ID=CLIENT_ID)

# 가입
@bp.route('/register', methods=['GET'])
def register():
    return render_template('register.html')

# 로그인
@bp.route('/login', methods=['GET'])
def login():
    CLIENT_ID = os.environ['CLIENT_ID']
    CALLBACK_URL = os.environ['CALLBACK_URL']
    SERVICE_URL = os.environ['SERVICE_URL']

    return render_template('login.html', CLIENT_ID=CLIENT_ID, CALLBACK_URL=CALLBACK_URL, SERVICE_URL=SERVICE_URL)
