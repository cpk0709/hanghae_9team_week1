from dotenv import load_dotenv
from bson import ObjectId
import jwt
import os

SECRET_KEY = 'SPARTA'

def tokenCheckProcess(token):
    load_dotenv(verbose=True)

    from pymongo import MongoClient
    url = os.getenv('MONGO_DB_URL')
    client = MongoClient(url)
    db = client.calendar

    try:
        # jwt.encode()로 인코딩한 JWT의 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        # payload에서 id를 꺼내와서 DB에서 user의 정보 가져오기(pw제외)
        userInfo = db.user.find_one({"id": payload["id"]},{'pw':0})

        # userInfo에 실제 user DB정보를 전달
        return {'result': 'success', 'userInfo':userInfo}

    except jwt.ExpiredSignatureError:
        return {'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'}

    # 유효하지 않은 토큰
    except jwt.exceptions.DecodeError:
        return {'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'}