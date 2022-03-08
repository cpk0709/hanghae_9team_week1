from pymongo import MongoClient
from dotenv import load_dotenv
import os
from flask import make_response

#!!!!!!!!!!!!매우 큰 에러 존재 exception 못잡음!!!!!!!!!!!!!!!!!!!
#단순 Connection만 제공하는 함수
def getConnection():
    #환경변수 설정
    load_dotenv(verbose=True)
    #dotenv_path: .env 파일의 절대경로 및 상대경로
    #stream: .env 파일 내용에 대한 StringIO 객체
    #verbose: .env 파일 누락 등의 경고 메시지를 출력할 것인지에 대한 옵션
    #override: 시스템 환경변수를 .env 파일에 정의한 환경변수가 덮어쓸지에 대한 옵션

    try:
        # mongoDB connection
        url = os.getenv('MONGO_DB_URL')
        client = MongoClient(url)
    except Exception as e:
        print(e)
        return {"msg": "db connection error"}

    return client

