# 데이터 베이스를 연결했으면 엔티티 즉, model을 만들어줘야 함.
# 근데 crud와 관련된 model을 만들것이므로 crud 파일 안에 만들어줌.

# 이 경로에 들어있는 db만 import 해주는 거임. 
# import apps.app은 그 안에 있는 모든 걸 갖다 쓸 거라는 말임.
# 이 db는 기본적으로 필요한 애임. 얘는 무조건 필요한 거고 밑에 있는 애들은 필요에 따라 가져오는 애들임.
from apps.app import db

# 이거는 시간과 날짜를 가져다 쓸 예정이기 때문에 import 한 거임.
from datetime import datetime

# 비밀번호 암호화 해주는 애임.
from werkzeug.security import generate_password_hash

# db.Model에 있는 걸 상속받아서 User라는 엔티티를 만들거임.
# 파이썬에서 상속은 괄호 안에다가 써줌.
class User(db.Model):

  # 테이블명 설정
  __tablename__ = 'users'

  # 컬럼 설정

  # id는 클래스에 대한 멤버변수임.
  # db의 컬럼으로 쓸 거고 자료형은 Integer로 할 거고 기본키 컬럼을 쓸 거임.
  id = db.Column(db.Integer, primary_key=True)

  # 얘는 문자열로 할 거고 글자수는 255자까지 되도록 할 거임.
  # index를 True로 해준 이유는 검색능력 향상을 위해서 해준거임. 굳이 안 해도 되고 필요하면 써도 되는 거임.
  # 기본키 컬럼이면 저 index는 자동으로 만들어줌.
  username = db.Column(db.String(255), index=True)

  # unique로 중복 불가 설정 해놓음.
  email = db.Column(db.String(255), unique=True, index=True)
  password_hash = db.Column(db.String(255))

  # Datetime을 자료형으로 한 거임. 그리고 등록하는 그 시간이 기본값으로 자동으로 들어가게 설정해줌.
  # default에 쓴 datetime은 위에 import한 파이썬에서 기본으로 제공해주는 datetime을 말하는 거임.
  created_at = db.Column(db.DateTime, default=datetime.now)

  # 특정 레코드가 변경됐을 때 변경 된 순간 그 시간이 다시 등록되게 해주셈 한 거임.
  updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)



  # 이 객체에서 사용할 수 있는 메서드를 만들기 위한 거임.
  # user라는 객체를 생성해서 이 함수를 사용하고 싶으면 user.password라고 쓸수 있게 해주는 데코레이션임.
  @property
  def password(self):
    # raise는 예외 처리해주는 거임.(java에서 new Exeption 한 거랑 같은 거임.)
    # user.password로 가져오는 것, 즉, getter를 못하게 막아주는 거임.
    # 그래서 결국에는 쓰기 전용으로 만들어줘라 하는 거임.
    raise AttributeError('비밀번호는 접근이 불가능 합니다.')
  

  # 위에 있는 password 함수를 사용하기 위한 setter기 때문에 password.setter가 들어가는 거임.
  @password.setter
  def password(self, password):
    # self는 이 파일 안 즉, 자기 자신을 말하는 거임.
    # generate 어쩌구는 비밀번호를 암호화해주는 거임.
    # password는 전달받은 비밀번호를 가르키는 거임.
    # java에서 많이 쓴 setter 같은 거임.
    self.password_hash = generate_password_hash(password)