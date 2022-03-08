from datetime import datetime, timedelta
from dotenv import load_dotenv
from bson import ObjectId
import jwt
import os
import hashlib

SECRET_KEY = 'SPARTA'

def signInProcess(id, pw):
    load_dotenv(verbose=True)

    from pymongo import MongoClient
    url = os.getenv('MONGO_DB_URL')
    client = MongoClient(url)
    db = client.calendar

    # 해시 암호화시
    pw = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    # DB에서 유저 찾기(없으면 None)
    result = db.user.find_one({'id': id, 'pw': pw})
    _id = str(result['_id'])

    # 내가 연결된 캘린더 ID 목록 가져오기
    calendarIds = list(db.team.find({'userid':_id},{'_id':0, 'userid':0}))
    calendarId = ''
    for cal in  calendarIds:
        # 내가 연결된 캘린더 ID중에 이름이 '나의 캘린더'인 캘린더의 식별값(_id) 조회
        myCalendarId = db.calendar.find_one({ '_id': ObjectId(cal['calendarid']), 'name':'나의 캘린더' })
        if myCalendarId is not None:
            calendarId = str(myCalendarId['_id'])

    # 유저 찾기 성공하면
    if result is not None:
        payload = {
         'id': id,
         'calendarId': calendarId,
         'exp': datetime.utcnow() + timedelta(seconds=5)  # 24시간(60*60*24)
        }
        # JWT 토큰 발행
        # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return {'result': 'success', 'token': token, 'calendarId': calendarId, 'msg': '로그인에 성공하였습니다.'}
    # 찾지 못하면(None이면)
    else:
        return {'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'}