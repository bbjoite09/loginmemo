
import os
from dotenv import load_dotenv
from flask import Flask

from pymongo import MongoClient


# .env 파일을 환경변수로 설정
load_dotenv()
# 환경변수 읽어오기
JWT_SECRET = os.environ['JWT_SECRET']
CLIENT_ID = os.environ['CLIENT_ID']
CALLBACK_URL = os.environ['CALLBACK_URL']
SERVICE_URL = os.environ['SERVICE_URL']
MONGODB_HOST = os.environ['MONGODB_HOST']
SENTRY = os.environ['SENTRY']
# mongodb 추가
client = MongoClient(MONGODB_HOST)
db = None


# 플라스크 프레임워크에서 지정한 함수 이름
# 플라스크 동작시킬 때 create_app() 함수의 결과로 리턴한 앱을 실행시킨다
def create_app(database_name='sparta'):
    import sentry_sdk
    from flask import Flask
    from sentry_sdk.integrations.flask import FlaskIntegration
    # 센트리 설정
    # DSN는 비노출
    # 환경 분리 필요(테스트에 들어가면 텟트 결과가 센트리 리포팅 = 비용)
    sentry_sdk.init(
        dsn=SENTRY,
        integrations=[FlaskIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

    # 플라스크 웹 서버 생성하기
    app = Flask(__name__)

    # 파이썬 중급 - 전역 변수를 함수 내부에서 수정 가능하게 만들어줌
    global db
    db = client.get_database(database_name)

    from app.views import api, main, memo, user

    app.register_blueprint(api.bp)
    app.register_blueprint(main.bp)
    app.register_blueprint(memo.bp)
    app.register_blueprint(user.bp)

    return app