from flask import Flask, render_template, request, redirect, url_for, flash
from email_validator import validate_email, EmailNotValidError
import logging
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_mail import Mail, Message
# render_template는 html 파일을 리턴 시켜주는 함수를 임폴트한거임.
# 스프링에서는 애플리케이션 쪽에 뷰리졸버 설정을 해준게 있었기 때문에 그냥 파일 이름만 써도 알아서 잘 받아왔던 거였음.
# 하지만 여긴 그런 게 없기 때문에 render_template를 임폴트해줘야 함.
# 화면단을 구성하는 파일이름은 무조건 template라고 되어 있어야 함. 그 이유는 render_template가 기본적으로 template이름을 읽기 때문임.
# os는 .env 파일에 있는 것들을 가져오기 위한 거임.


app = Flask(__name__)

# 시크릿키 설정
app.config['SECRET_KEY'] = '1234'
# 환경변수 관련된 건 대문자로 써줘야함.

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

# mail관련 설정 추가
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER') # 이렇게 하면 .env에 설정했던 거 가져와줌.
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# 로그 레벨 설정
app.logger.setLevel(logging.DEBUG) # 개발단계에서는 보통 DEBUG로 함. <모든 로그가 다 출력 됨.>

# 로그 출력
# app.logger.critical('치명적오류')
# app.logger.error('오류')
# app.logger.warning('경고')
# app.logger.info('info')
# app.logger.debug('debug')

@app.route('/')
def index():
  return 'Hello Flaskff'

@app.route('/hi/<name>') # <> 안에다가 담아줄 값의 변수명을 써주면 됨. 
  #경로에다가 필요한 정보를 담아서 보낼때 저렇게 하는 거임.
def hi(name): # 매개변수 써준 거임.
  # return f'hi {name}' # 경로 뒤에 보내준 값이 그대로 여기에 출력됨.
  return render_template('index.html', name=name) # 앞에 이름이 변수명이고 뒤에 name이 값임.

@app.route('/contact')
def contact():
  # 이렇게 하면 단순 페이지 이동만 되는 라우터가 되는 거임.
  return render_template('contact.html')




# contact 페이지에서 문의사항을 작성하고 전송버튼을 누르면 서버로 해당 내용이 전송(POST)
# 그리고 전송이 완료 되면 전송완료 페이지로 이동(GET) 하도록 구현할거임.


# get, post 뭐로 요청하든 다 contact_complete 함수가 실행되도록 하는 거임.
@app.route('/contact/complete', methods=['GET', 'POST'])
def contact_complete():
  if request.method == 'POST': # request는 요청 객체임. import 해줘야 함.
    # .method하면 요청 메서드가 들어감.

    # POST 요청 시 처리할 코드들
    # form 태그에 담겨져 있는 것들을 꺼내는 거 할거임.
    username = request.form['username']
    email = request.form['email']
    description = request.form['description']

    is_vali = True # 검사해서 검사한 결과에 만족하지 않으면 False로 바꿀거임.

    if not username: # 파이썬은 해당 변수명에 값이 없으면 false임.
      flash('이름은 반드시 입력하세요')
      is_vali = False

    if not email:
      flash('이메일은 반드시 입력해야함')
      is_vali = False

    try:
      validate_email(email) # 얘는 해당 값이 이메일 형식을 가지고 있는지 확인하는 애임.
    except EmailNotValidError: # 얘는 이메일 형식을 가지고 있지 않으면 표시되는 거임.
      flash('이메일 형식에 맞게 작성')
      is_vali = False

    if not description:
      flash('내용은 반드시 입력')
      is_vali = False

    if not is_vali: # is_vali가 False면 뭔가 잘못됐다는 뜻이니까 그냥 해당 페이지에 그대로 있는 거임.
      return redirect(url_for('contact'))

    send_mail(email, "문의 확인용 메일", "mail_form", username=username, description=description)

    # 위에 코드가 실행된 후 다시 contact_complete 함수로 돌아가게 함.
    # Post 요청을 해서 다시 이 함수로 돌아오게 되면 그때는 Post 요청이 아니라 Get 요청일거기 때문에
    # 밑에 render_template이 실행되는 거임.
    # redirect를 사용 안하고 Route로 처리하고 페이지에서 뒤로가기 처리하면 전송 요청하는 그 함수로 돌아가기 때문에 기간 만료되었습니다. 이런 페이지가 뜸.
    # 그런 거 뜨지 않게 하기 위해서 이렇게 하는 거임.
    flash('빠르게 답변 드리겠습니다.')
    return redirect(url_for('contact_complete')) # url_for에다가는 함수이름 쓰는 거임.

  return render_template('contact_complete.html') # GET 요청을 하면 이 코드가 실행 됨.


# 메일 전송처리 해주는 함수
def send_mail(to, subject, template, **kwargs):
  # 매개변수를 세팅할 때 몇 갠 지 모르겠을 때 **kwargs 해주면 됨.
  msg = Message(subject, recipients=[to]) # 대괄호 쳐줘야 함. 받는 사람 이메일 주소가 들어가게 되는 거임.
  msg.body = render_template(template + '.txt', **kwargs) # 메일 종류에 따라서 txt 파일만 받을 수 있는 메일이 있기 때문에 이렇게 되는 거임.
  msg.html = render_template(template + '.html', **kwargs)
  mail.send(msg)
