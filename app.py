from python.calendar.createCalendar import createCalendarProcess
from python.calendar.deleteCalendar import deleteCalendarProcess
from python.calendar.getCalendarIdList import getCalendarListProcess
from python.calendar.getMyCalendarId import getMyCalendarIdProcess2
from python.calendar.inviteCalendar import  createInviteLinkProcess
from python.post.createPost import createPostProcess
from python.post.deletePost import deletePostProcess
from python.post.editPost import editPostProcess
from python.user.signUp import signUpProcess
from datetime import datetime, timedelta
from python.calendar.getCalendar import getCalendarProcess
import jwt
from flask import Flask, render_template, request, jsonify, redirect, make_response, json, url_for
from python.user.signUp import signUpProcess
from python.user.signIn import signInProcess
from python.user.tokenCheck import tokenCheckProcess
from python.user.getUserInfo import getUserInfoProcess
from python.user.tokenMiddleware import token_required
from bson import json_util
import os


app = Flask(__name__, static_url_path='/static')

SECRET_KEY = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    token = request.cookies.get('myToken')
    # 토큰 유효성 체크
    tokenMsg = tokenCheckProcess(token)
    if tokenMsg['result'] == 'success':
        calendarId = request.cookies.get('calendarId')
        # 사용자 정보 가져오기
        userInfo = getUserInfoProcess(tokenMsg['id'])
        # return render_template('index.html', userInfo=userInfo)
        return render_template('main.html', userInfo=userInfo) #Jinja2에서 사용자정보 활용가능
    elif tokenMsg['result'] == 'fail' and tokenMsg['msg'] == '로그인 시간이 만료되었습니다.':
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/api/user/signUp', methods=["POST"])
def signUp():
    print('!!@@')
    id = request.form['id']
    pwOne = request.form['pwOne']
    pwTwo = request.form['pwTwo']
    nickname = request.form['nickname']

    msg = signUpProcess(id, pwOne, pwTwo, nickname)
    return jsonify(msg)

@app.route('/signin')
def signIn():
    return render_template('signin.html')

@app.route('/render')
def render():
    return render_template('signup.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/api/user/signIn', methods=['POST'])
def signInJwt():
    id = request.form['id']
    pw = request.form['pw']

    msg = signInProcess(id, pw)
    resp = make_response(jsonify(msg))
    if msg['result']=='success':
        # 개인캘린더id 가져오기
        calendarId = getMyCalendarIdProcess2(msg['nickname'])
        # 응답 딕셔너리에 추가
        msg['calendarId'] = calendarId
        # 백엔드에서 쿠키 저장
        resp.set_cookie('id', id)
        resp.set_cookie('myToken', msg['token'])
        resp.set_cookie('calendarId', calendarId)
        return resp
    else:
        return resp

@app.route('/api/user/logout')
def logout():
    resp = make_response(render_template('index.html'))
    # resp = make_response(url_for('home'))
    resp.delete_cookie('mytoken')
    resp.delete_cookie('id')
    resp.delete_cookie('calendarId')
    return resp

@app.route('/api/calendar/list', methods=['GET'])
def getCalendarList():
  
    id = request.args.get('id')

    result = getCalendarListProcess(id)

    return jsonify(result)


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

@app.route('/api/calendar/createLink', methods=['POST'])
def createLink():
    calendarId = request.form['calendarId']

    result = createInviteLinkProcess(calendarId)

    return jsonify(result)

@app.route('/api/calendar/invite', methods=['POST'])
def inviteCalendar():
    # calendarId = request.args.get('calendarId')

    token = request.cookies.get('myToken')
    print(token)
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    print(payload)
    userId = payload['id']
    print(userId)

    # result = createInviteLinkProcess(calendarId, userId)

    # return jsonify(result)
    return jsonify({'1':'1'})

@app.route('/api/calendar/post/new', methods=['POST'])
def createPost():
    calendarId = request.form['calendarId']
    dateTime = request.form['dateTime']
    content = request.form['content']
    nickname = request.form['nickname']

    result = createPostProcess(calendarId, dateTime, content, nickname)

    return jsonify(result)

@app.route('/api/calendar/post/edit', methods=['POST'])
def editPost():
    calendarId = request.form['calendarId']
    dateTime = request.form['dateTime']
    content = request.form['content']
    nickname = request.form['nickname']
    result = editPostProcess(calendarId, dateTime, content, nickname)
    return jsonify(result)

@app.route('/api/calendar/post/delete', methods=['POST'])
def deletePost():
    token = request.cookies.get('mytoken')
    tokenMsg = tokenCheckProcess(token)
    if tokenMsg['result'] == 'success':
        postId = request.form['postId']

        result = deletePostProcess(postId)

        return jsonify(result)
    else:
        return {"result": "no token"}

@app.route('/test')
@token_required
def tokenMiddlewareTest():
    return render_template('main.html')

# 라우터에서 토큰확인하는 쌤플코드
@app.route('/sample')
def noMiddleSample():
    token = request.cookies.get('mytoken')
    tokenMsg = tokenCheckProcess(token)
    if tokenMsg['result'] == 'success':
        # 라우터 기존코드 실행
        userInfo = getUserInfoProcess(tokenMsg['id'])
        return render_template('main.html', userInfo=userInfo) #jinja2에서 사용자정보 활용가능
    else:
        return redirect(url_for("signIn"))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



