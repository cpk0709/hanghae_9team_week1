from pymongo import MongoClient
from dotenv import load_dotenv
import os
import hashlib

#회원가입 프로세스
def signUpProcess(id, pw, nickName):
    #환경변수 설정
    load_dotenv(verbose=True)
    #dotenv_path: .env 파일의 절대경로 및 상대경로
    #stream: .env 파일 내용에 대한 StringIO 객체
    #verbose: .env 파일 누락 등의 경고 메시지를 출력할 것인지에 대한 옵션
    #override: 시스템 환경변수를 .env 파일에 정의한 환경변수가 덮어쓸지에 대한 옵션

    try:
        #mongoDB connection
        url = os.getenv('MONGO_DB_URL')
        client = MongoClient(url)
        db = client.ourschedule

        #중복된 아이디 닉네임 체크
        isUser = db.user.find_one({'id':id})
        if isUser is not None:
            return {'msg': 'existId'}
        isNickName = db.user.find_one({'nickName': nickName})
        if isNickName is not None:
            return {'msg': 'existNickName'}

        #DB에 user 추가 + pw 암호화 후 저장
        user = {
            'id': id,
            'pw': hashlib.sha256(pw.encode('utf8')).hexdigest(),
            'nickName': nickName
        }
        db.user.insert_one(user)

    except Exception as e:
        print(e)
        return {'msg': 'dbError'}

    return {'msg': 'success'}



