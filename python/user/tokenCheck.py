import jwt
import os

SECRET_KEY = os.getenv('SECRET_KEY')

def tokenCheckProcess(token):

    try:
        # jwt.encode()로 인코딩한 JWT의 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # DB에서 user정보 가져오기(pw제외) -> 모듈(getUserInfo.py)로 변경
        # userInfo = db.user.find_one({"id": payload["id"]},{'pw':0})

        # userInfo에 user정보를 전달 -> id만 전달
        # return {'result': 'success', 'userInfo':userInfo}
        return {'result': 'success', 'id': payload['userId']}

    except jwt.ExpiredSignatureError:
        return {'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'}

    # 유효하지 않은 토큰
    except jwt.exceptions.DecodeError:
        return {'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'}
