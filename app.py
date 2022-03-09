from python.calendar.createCalendar import createCalendarProcess
from python.calendar.deleteCalendar import deleteCalendarProcess
from python.calendar.getCalendarIdList import getCalendarIdListProcess, getCalendarListProcess
from python.calendar.getMyCalendarId import getMyCalendarIdProcess
from python.calendar.inviteCalendar import  createInviteLinkProcess
from python.post.createPost import createPostProcess
from python.post.deletePost import deletePostProcess
from python.user.signUp import signUpProcess
from datetime import datetime, timedelta
from python.calendar.getCalendar import getCalendarProcess
import jwt
from flask import Flask, render_template, request, jsonify, redirect, make_response, json
from python.user.signUp import signUpProcess
from python.user.signIn import signInProcess
from python.user.tokenCheck import tokenCheckProcess
from python.user.getUserInfo import getUserInfoProcess
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
        calendarIdList = request.cookies.get('calendarIdList')
        dictCalendarIdList = json.loads(calendarIdList) # str->dict
        # 사용자 정보 가져오기
        userInfo = getUserInfoProcess(tokenMsg['id'])
        # return render_template('index.html', userInfo=userInfo, calendarIdList=dictCalendarIdList)
        # return render_template('main.html?calendarId='+calendarId, userInfo=userInfo, calendarIdList=dictCalendarIdList)
        return render_template('main.html', userInfo=userInfo, calendarIdList=dictCalendarIdList)
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
    resp = make_response(jsonify(msg))
    if msg['result']=='success':
        # 로그인성공시 캘린더id들 가져오기
        calendarIdList = getCalendarIdListProcess(msg['_id'])

        # 나의 개인 캘린더id 가져오기
        calendarId = getMyCalendarIdProcess(calendarIdList, msg['nickname'])
        # 응답 딕셔너리에 추가
        msg['calendarId'] = calendarId

        # 백엔드에서 쿠키 저장
        resp.set_cookie('id', id)
        resp.set_cookie('myToken', msg['token'])
        resp.set_cookie('calendarId', calendarId)
        # 캘린더ID List를 쿠키로 보내기위해 str로 변환하는 과정(쿠키는 str만 가능)
        calendarIdList = {"calendarIdList": calendarIdList}
        # ObjectId('') is not JSON serializable의 해결방법
        # {'calendarid': ObjectId('62273cd907b346c1eedbe9c5')} -> {'calendarid': {'$oid': '62273cd907b346c1eedbe9c5'}}
        calendarIdList = json.loads(json_util.dumps(calendarIdList))
        resp.set_cookie('calendarIdList', json.dumps(calendarIdList))
        return resp
    else:
        return resp

@app.route('/api/calendar/list', methods=['GET'])
def getCalendarList():
    id = request.form['id']
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
    calendarId = request.args.get('calendarId')

    token = request.cookies.get('myToken')
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    userId = payload['id']

    result = createInviteLinkProcess(calendarId, userId)

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



