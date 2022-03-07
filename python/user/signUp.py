from pymongo import MongoClient
from dotenv import load_dotenv
import os

def signUpProcess(id, pw, nickName):
    load_dotenv(verbose=True)
    #dotenv_path: .env 파일의 절대경로 및 상대경로
    #stream: .env 파일 내용에 대한 StringIO 객체
    #verbose: .env 파일 누락 등의 경고 메시지를 출력할 것인지에 대한 옵션
    #override: 시스템 환경변수를 .env 파일에 정의한 환경변수가 덮어쓸지에 대한 옵션

    try:

        url = os.getenv('MONGO_DB_URL')

        client = MongoClient(url)
        db = client.ourschedule

        user = {
            'id': id,
            'pw': pw,
            'nickName': nickName
        }
        db.user.insert_one(user)
    except Exception as e:
        print(e)
        return {'msg': 'dbError'}

    return {'msg': 'success'}




# db.user.insert_one({'name': 'woong'})

