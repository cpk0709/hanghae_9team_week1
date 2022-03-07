from flask import Flask, render_template, request, jsonify
from python.user.signUp import signUpProcess
from python.user.signIn import signInProcess
from datetime import datetime, timedelta
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
    user = request.get_json()

    msg = signUpProcess(user['id'], user['pw'], user['nickName'])
    return jsonify(msg)

@app.route('/signin')
def signInPage():
    return render_template('signin.html')

@app.route('/api/user/signIn', methods=['POST'])
def signIn():
    id = request.form['id']
    pw = request.form['pw']

    msg = signInProcess(id, pw)
    return jsonify(msg)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)



