from flask import Blueprint, render_template, redirect, url_for

from apps.crud.forms import UserForm
from apps.crud.models import User
from apps.app import db

# 첫번째는 Blueprint 이름인데 보통 기능 이름으로 함.
# 두 번째는 이 블루스크린의 경로를 알려주는 거임.
crud = Blueprint("crud", __name__, template_folder="templates", static_folder="static")

# crud라는 Blueprint를 만들었기 때문에 app.route가 아니라 crud.route가 됨.
@crud.route('/')
def index():
  return render_template('crud/index.html')

@crud.route('/users/new', methods=["GET", "POST"]) # 회원가입 페이지로 가기 위한 라우터 만들어주는 거임.
def create_user():
  form = UserForm() # Form에다가 만들어놓은 그 형식을 가져와서 쓸 거기 때문에 객체로 불러온 거임.
  # 객체를 생성하고 그 객체를 html 쪽으로 보내준 거임.

  print(form.username.data)
  print(form.email.data)
  print(form.password.data)

  if form.validate_on_submit(): # 유효성 검사에 성공했으면 true 실패하면 false가 됨. wtf에 원래 있는 거임.
    # db에 저장할 객체 설정
    user = User( # 객체를 생성할때 setter들이 호출됨. password_hash 라고 안 하고 그냥 password라고 해서 암호화가 된 거임.
      # password_hash라고 되어 있으면 그냥 고대로 들어가는 거임.
      username = form.username.data,
      email = form.email.data,
      password = form.password.data
    )

    # db에 insert 시키고
    db.session.add(user)
    db.session.commit()

    # 회원가입 완료 페이지 이동
    return redirect(url_for('crud.users'))

  return render_template('crud/create.html', form=form)

@crud.route('/users')
def users():
  # 회원정보를 db에서 가져오는 코드
  users = User.query.all()
  print(users)

  return render_template('crud/index.html', users=users)