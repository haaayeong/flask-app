from flask_wtf import FlaskForm # 화면에서 보여줄 수 있는 다양한 양식들을 파이썬으로 가지고 있음. 유효성 검사 기능까지 가지고 있음. 서버로 보내서 유효성 검사를 해주고 flash 메세지를 뱉어줌.ㄹ
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import length, DataRequired, Email

# FlaskForm 상속 받음. 입력받을 애들 세팅해주는 거임.
class UserForm(FlaskForm):
  username = StringField( # 얘 자체가 그냥 input 태그인 거임.
    "사용자명", # 얘가 label임.
    validators=[
      DataRequired(message='사용자명은 필수입니다.'), # 입력했는지 안했는지를 알아서 검사해주고 안 했으면 message 띄워주는 거임.
      length(max=30, message='30자 이하로 입력하세요') # 최대 30글자까지만 입력 가능. 이 조건에서 벗어나면 message 띄워줌.
    ]
  )

  email = StringField(
    "메일주소",
    validators=[
      DataRequired(message='이메일은 필수로 입력하셔야 합니다.'),
      Email(message='메일 주소 형식으로 입력') # email 형식인지 아닌지 알아서 검사해줌.
    ]
  )

  password = PasswordField( # input 타입이 password로 되어있는 애인거임.
    "비밀번호",
    validators=[
      DataRequired(message='비밀번호는 반드시 입력')
    ]
  )

  submit = SubmitField('회원가입') # submit 버튼을 만들어준 거임.


  # 이런 식으로 만든 거 하나하나가 다 html에 들어가는 거라고 생각하면 되는 거임. 그렇게 되면서 걸려있는 유효성 검사까지 알아서 해주는 거임.