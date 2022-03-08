from flask import Flask, render_template, request, jsonify, redirect
from python.user.signUp import signUpProcess
from python.user.signIn import signInProcess
from python.user.tokenCheck import tokenCheckProcess

app = Flask(__name__, static_url_path='/static')

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.zee7s.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

SECRET_KEY = 'SPARTA'

@app.route('/')
def home():
    token = request.cookies.get('myToken')
    calendarId = request.cookies.get('calendarId')
    print('나의캘린더id: ', calendarId)

    tokenMsg = tokenCheckProcess(token)
    if tokenMsg['result'] == 'success':
        return render_template('index.html', userInfo=tokenMsg['userInfo'])
        # return render_template('나의캘린더.html?calendarId='+calendarId, userInfo=tokenMsg['userInfo'])
    elif tokenMsg['result'] == 'fail' and tokenMsg['msg'] == '로그인 시간이 만료되었습니다.':
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/api/user/signUp', methods=["POST"])
def signUp():
    user = request.get_json()

    msg = signUpProcess(user['id'], user['pw'], user['nickName'])
    return jsonify(msg)

@app.route('/signin')
def signIn():
    return render_template('signin.html')

@app.route('/api/user/signIn', methods=['POST'])
def signInJwt():
    id = request.form['id']
    pw = request.form['pw']

    msg = signInProcess(id, pw)
    return jsonify(msg)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



