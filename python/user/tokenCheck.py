import jwt
import os

SECRET_KEY = os.getenv('SECRET_KEY')


#로그인이 되어있는지 확인하는 서비스
def tokenCheckProcess(token):

    try:
        # jwt.encode()로 인코딩한 JWT의 디코딩
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])

        return {'result': 'success', 'id':payload['userId']}
    #토큰 시간이 만료시
    except jwt.ExpiredSignatureError:
        return {'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'}

    # 유효하지 않은 토큰
    except jwt.exceptions.DecodeError:
        return {'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'}
