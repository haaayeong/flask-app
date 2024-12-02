import secrets # 암호화키를 만들어주는 모듈임.
import os

dir = os.path.dirname(__file__)

# 모든 환경에서 쓰는 환경설정을 작성해줌.
class BaseConfig:
  SECRET_KEY = secrets.token_urlsafe(32) # 랜덤한 문자열이 32byte 짜리로 만들어지게 되는 거임.
  WTF_CSRF_SECRET_KEY = secrets.token_urlsafe(32)

# 위에 코드까지는 공통적으로 사용하는 환경설정을 세팅해준 거임.

# BaseConfig 상속받은 거임.
# 로컬환경에서 반영되는 환경설정 클래스
class LocalConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(dir,"test.db")}' # sqlite는 경량 데이터 베이스임.
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=True

# Test 환경이랑 Local 환경이랑 달리질 게 없기 때문에 그냥 똑같이 적어줌.
# 만약 다르면 다른 거 추가해주거나 바꿔줘야함.
class TestingConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:1234@localhost:3306/flaskdb'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=True  

# 배포단계에서의 환경설정
# 여기서는 아마 배포 주소가 달라져야 할 거임.
# 하지만 지금은 배포 안 하니까 그냥 똑같이 적어줌.
class ProductionConfig(BaseConfig):
  SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:1234@localhost:3306/flaskdb'
  SQLALCHEMY_TRACK_MODIFICATIONS=False
  SQLALCHEMY_ECHO=True

# dictionary를 만들어서 각각 환경에 쓸 클래스들을 설정 해준 거임.
# 여기서 세팅해준 거를 선택해서 쓰면 되는 거임.
config = {
  "local" : LocalConfig,
  "testing" : TestingConfig,
  "production" : ProductionConfig
}
