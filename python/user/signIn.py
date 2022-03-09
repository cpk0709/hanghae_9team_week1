from datetime import datetime, timedelta
from python.database.mongoDB import getConnection
import jwt
import os
import hashlib

def signInProcess(id, pw):
    client = getConnection()
    db = client.ourschedule

    pw = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    # DB에서 유저 찾기(없으면 None)
    result = db.user.find_one({'id': id, 'pw': pw})

    # 유저 찾기 성공하면
    if result is not None:
        _id = str(result['_id'])
        nickname = str(result['nickname'])

        payload = {
         'userId': id,
         # 'calendarId': calendarId,
         'exp': datetime.utcnow() + timedelta(60*60*24)  # 24시간(60*60*24)
        }
        # JWT 토큰 발행
        SECRET_KEY = os.getenv('SECRET_KEY')
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        # return {'result': 'success', 'token': token, 'calendarId': calendarId, '_id':_id, 'msg': '로그인에 성공하였습니다.'}
        return {'result': 'success', 'token': token, '_id':_id, 'nickname':nickname, 'msg': '로그인에 성공하였습니다.'}
    # 찾지 못하면(None이면)
    else:
        return {'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'}

    client.close()