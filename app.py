from python.calendar.createCalendar import createCalendarProcess
from python.calendar.deleteCalendar import deleteCalendarProcess
from python.calendar.getCalendarIdList import getCalendarListProcess
from python.calendar.getMyCalendarId import getMyCalendarIdProcess2
from python.calendar.inviteCalendar import createInviteLinkProcess, inviteCalendarProcess
from python.calendar.checkCalendarId import checkCalendarIdProcess
from python.calendar.getCalendar import getCalendarProcess
from python.post.createPost import createPostProcess
from python.post.deletePost import deletePostProcess
from python.post.editPost import editPostProcess
from python.user.signUp import signUpProcess
from python.user.signIn import signInProcess
from python.user.tokenCheck import tokenCheckProcess
from python.user.getUserInfo import getUserInfoProcess

import os
from flask import Flask, render_template, request, jsonify, redirect, make_response, url_for


app = Flask(__name__, static_url_path='/static')

SECRET_KEY = os.getenv('SECRET_KEY')

@app.route('/')
def home():
    token = request.cookies.get('myToken')
    # 토큰 유효성 체크
    tokenMsg = tokenCheckProcess(token)

    if tokenMsg['result'] == 'success':
        userInfo = getUserInfoProcess(tokenMsg['id'])          # 사용자 정보 가져오기
        return render_template('main.html', userInfo=userInfo) # Jinja2 사용자정보 활용
    elif tokenMsg['result'] == 'fail' and tokenMsg['msg'] == '로그인 시간이 만료되었습니다.':
        return render_template('signin.html')
    else:
        return render_template('signin.html')


@app.route('/render')
def render():
    return render_template('signup.html')


@app.route('/signin')
def signIn():
    # 토큰확인 후 로그인되어있으면 main으로 이동
    token = request.cookies.get('myToken')

    if token is not None:
        tokenMsg = tokenCheckProcess(token)
        if tokenMsg['result'] == 'success':
            return redirect(url_for("main"))
        else:
            return tokenMsg
    else:
        return render_template('signin.html')


@app.route('/main', methods=['GET'])
def main():
    token = request.cookies.get('myToken')
    tokenMsg = tokenCheckProcess(token)

    if tokenMsg['result'] == 'success':
        calendarId = request.args.get("calendarId")
        userInfo = getUserInfoProcess(tokenMsg['id'])

        if calendarId is not None and calendarId is not "":
            # 캘린더ID가 DB에 존재하는지 조회
            checkResult = checkCalendarIdProcess(calendarId)

            if checkResult['msg']=="Existed":
                resp = make_response(render_template('main.html', userInfo=userInfo, myCalendarId=calendarId))
                resp.set_cookie('calendarId', calendarId)
            else:
                # 존재하지 않는 캘린더ID로 접근시 404페이지 표시
                resp = make_response(render_template('error404.html'))
        else:
            resp = make_response(render_template('main.html', userInfo=userInfo))
        return resp
    else:
        return redirect(url_for("signIn"))


@app.route('/api/user/signUp', methods=["POST"])
def signUp():
    id = request.form['id']
    pwOne = request.form['pwOne']
    pwTwo = request.form['pwTwo']
    nickname = request.form['nickname']

    msg = signUpProcess(id, pwOne, pwTwo, nickname)
    return jsonify(msg)


@app.route('/api/user/signIn', methods=['POST'])
def signInJwt():
    id = request.form['id']
    pw = request.form['pw']

    msg = signInProcess(id, pw)
    resp = make_response(jsonify(msg))
    
    if msg['result']=='success':
        # 개인캘린더id 가져와서 응답 딕셔너리에 추가
        calendarId = getMyCalendarIdProcess2(msg['nickname'])
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
    resp = make_response(redirect(url_for("main")))
    resp.delete_cookie('myToken')
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


@app.route('/api/calendar/invite', methods=['GET'])
def inviteCalendar():
    calendarId = request.args.get('calendarId')
    userId = request.cookies.get('id')

    result = inviteCalendarProcess(calendarId, userId)

    return render_template('invite.html', info=result)


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
    postId = request.form['postId']

    result = editPostProcess(calendarId, dateTime, content, postId)
    
    return jsonify(result)


@app.route('/api/calendar/post/delete', methods=['POST'])
def deletePost():
    token = request.cookies.get('myToken')
    tokenMsg = tokenCheckProcess(token)

    if tokenMsg['result'] == 'success':
        postId = request.form['postId']
        result = deletePostProcess(postId)
        return jsonify(result)
    else:
        return {"result": "no token"}


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



