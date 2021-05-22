import datetime
import hashlib
import os

import jwt
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# mongodb 추가
client = MongoClient('localhost', 27017)
db = None

# 플라스크 프레임워크에서 지정한 함수 이름
# 플라스크 동작시킬 때 create_app() 함수의 결과로 리턴한 앱을 실행시킨다.
def create_app(database_name='sparta'):
    # 플라스크 웹 서버 생성하기
    app = Flask(__name__)

    global db
    db = client.get_database(database_name)


    from views import api, main, memo, user

    app.register_blueprint(api.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(memo.bp)
    app.register_blueprint(user.bp)

    return app





