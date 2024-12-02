from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_login

from apps.config import config # config라는 파이썬 파일에 들어있는 config를 불러올거임.
import os

config_key = os.environ.get('FLASK_CONFIG_KEY') # .env에 입력한 값을 가져오는 거임.

# SQLAlchemy 객체 생성
db = SQLAlchemy()

# CSRF 객체 생성
csrf = CSRFProtect()

# 로그인 관련된 기초 작업임.
login_manager = 

def create_app():
  app = Flask(__name__) # 플라스크 객체를 생성하는 것. __name__은 현재 실행 중인 모듈 이름을 전달하는 것임.

  #MySQL 연결
  # app.config.from_mapping(
  #   SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:1234@localhost:3306/flaskdb',
  #   SQLALCHEMY_TRACK_MODIFICATIONS=False,
  #   SQLALCHEMY_EHCO=True,
  #   SECRET_KEY='1234',
  #   WTF_CSRF_SECRET_KEY='1234'
  # ) 
  # root:1234는 mysql 계정명이랑 비밀번호 작성해준거임.
  # 데이터베이스 주소 넣은거임. 배포하려고 주소 구매했으면 그거 넣어주면 됨.
  # 그 뒤는 데이터 베이스 이름임.
  # ehco는 실행되는 쿼리문을 콘솔창에 띄울 수 있게 하는 거임.
  # 그 위에 거는 객체가 변경된 변경사항을 감지를 못하게 막은 거임.
  # 그 이유는 하나하나 변경 될 때마다 추적을 하고 그럼 성능이 저하됨. 그래서 비활성화해둔거임.


  app.config.from_object(config[config_key])
  # 이렇게 해주면 여기서 힘들여가면서 찾지 않아도 그냥 .env 파일 들어가서 바꿔주기만 하면 됨.
  # 환경설정 어느 환경인지 설정해준 거임. 

  # 데이터베이스에 초기세팅을 해줄거고 app을 연결시켜준 거임.
  db.init_app(app)

  # 얘가 app과 db 연결해주세요 라고 한 거임.
  Migrate(app, db)

  from apps.crud import views as crud_views # 경로 잡아주고 모듈 가져오는 거임. 그리고 다른 블루프린트들과 헷갈릴 수 있으니까 별칭 달아줌.
  app.register_blueprint(crud_views.crud, url_prefix='/crud') # crud_views 안에 들어있는 crud를 가져올 거임.
  # 무조건 앞에 crud를 붙여야 한다고 설정 해놓음.

  return app # 세팅이 끝난 플라스크 앱을 리턴시켜주는 함수임.
