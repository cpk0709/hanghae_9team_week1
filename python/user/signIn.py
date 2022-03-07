from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import os
import hashlib

SECRET_KEY = 'SPARTA'

def signInProcess(id, pw):
    load_dotenv(verbose=True)

    from pymongo import MongoClient
    url = os.getenv('MONGO_DB_URL')
    client = MongoClient(url)
    db = client.dbsparta

    # 해시 암호화시
    pw = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    # DB에서 유저 찾기(없으면 None)
    result = db.users.find_one({'id': id, 'pw': pw})

    # 유저 찾기 성공하면
    if result is not None:
        payload = {
         'id': id,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        # JWT 토큰 발행
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return {'result': 'success', 'token': token, 'msg': '로그인에 성공하였습니다.'}
    # 찾지 못하면(None이면)
    else:
        return {'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'}