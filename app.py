
from flask import Flask, render_template, request, jsonify

from python.calendar.createCalendar import createCalendarProcess
from python.calendar.deleteCalendar import deleteCalendarProcess
from python.calendar.getCalendarIdList import getCalendarIdListProcess
from python.calendar.getMyCalendarId import getMyCalendarIdProcess
from python.post.createPost import createPostProcess
from python.post.deletePost import deletePostProcess
from python.user.signUp import signUpProcess
from datetime import datetime, timedelta
from python.calendar.getCalendar import getCalendarProcess
import jwt
from flask import Flask, render_template, request, jsonify, redirect
from python.user.signUp import signUpProcess
from python.user.signIn import signInProcess
from python.user.tokenCheck import tokenCheckProcess
import os


app = Flask(__name__, static_url_path='/static')

SECRET_KEY = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    token = request.cookies.get('myToken')
    calendarId = request.cookies.get('calendarId')
    print('나의캘린더id: ', calendarId) #

    tokenMsg = tokenCheckProcess(token) # 사용자info 프로세스 분리----------
    if tokenMsg['result'] == 'success':
        return render_template('index.html', userInfo=tokenMsg['userInfo'])
        # return render_template('나의캘린더.html?calendarId='+calendarId, userInfo=tokenMsg['userInfo'])
    elif tokenMsg['result'] == 'fail' and tokenMsg['msg'] == '로그인 시간이 만료되었습니다.':
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/api/user/signUp', methods=["POST"])
def signUp():
    id = request.form['id']
    pwOne = request.form['pwOne']
    pwTwo = request.form['pwTwo']
    nickname = request.form['nickname']


    msg = signUpProcess(id, pwOne, pwTwo, nickname)
    return jsonify(msg)

@app.route('/signin')
def signIn():
    return render_template('signin.html')

@app.route('/api/user/signIn', methods=['POST'])
def signInJwt():
    id = request.form['id']
    pw = request.form['pw']

    msg = signInProcess(id, pw)
    if msg['result']=='success':
        # 로그인성공시에 캘린더id들 가져오기
        calendarIdList = getCalendarIdListProcess(msg['_id'])

        # 나의 개인 캘린더id 가져오기
        calendarId = getMyCalendarIdProcess(calendarIdList, msg['nickname'])
        msg['calendarId'] = calendarId

    return jsonify(msg)

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



