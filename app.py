from flask import Flask, render_template, request, jsonify

from python.calendar.createCalendar import createCalendarProcess
from python.calendar.deleteCalendar import deleteCalendarProcess
from python.post.createPost import createPostProcess
from python.post.deletePost import deletePostProcess
from python.user.signUp import signUpProcess
from datetime import datetime, timedelta
from python.calendar.getCalendar import getCalendarProcess
import jwt


app = Flask(__name__, static_url_path='/static')

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.zee7s.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = 'SPARTA'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/user/signUp', methods=["POST"])
def signUp():
    id = request.form['id']
    pw = request.form['pw']
    nickname = request.form['nickname']


    msg = signUpProcess(id, pw, nickname)
    return jsonify(msg)

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/api/user/signIn', methods=['POST'])
def sign_in():
    # 로그인
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    # 해시 암호화시
    # pw_receive = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    # DB에서 유저 찾기
    result = db.users.find_one({'id': id_receive, 'pw': pw_receive})

    # 유저 찾기 성공하면
    if result is not None:
        payload = {
         'id': id_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        # JWT 토큰 발행
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token, 'msg': '로그인에 성공하였습니다.'})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/api/calendar/get', methods=['GET'])
def getCalendar():
    calendarId = request.args.get("calendarId")
    result = getCalendarProcess(calendarId)

    return jsonify(result)

@app.route('/api/calendar/new', methods=['POST'])
def createCalendar():
    name = request.form['name']
    owner = request.form['owner']

    result = createCalendarProcess(name, owner)

    return jsonify(result)

@app.route('/api/calendar/delete', methods=['POST'])
def deleteCalendar():
    calendarId = request.form['calendarId']

    result = deleteCalendarProcess(calendarId)

    return jsonify(result)

@app.route('/api/calendar/post/new', methods=['POST'])
def createPost():
    calendarId = request.form['calendarId']
    dateTime = request.form['dateTime']
    content = request.form['content']
    nickname = request.form['nickname']

    result = createPostProcess(calendarId, dateTime, content, nickname)

    return jsonify(result)

@app.route('/api/calendar/post/delete', methods=['POST'])
def deletePost():
    postId = request.form['postId']

    result = deletePostProcess(postId)

    return jsonify(result)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



