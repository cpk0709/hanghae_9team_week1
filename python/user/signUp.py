import hashlib
from python.database.mongoDB import getConnection

#회원가입 프로세스
def signUpProcess(id, pw, nickName):

    client = getConnection()
    db = client.ourschedule
    try:
        #중복된 아이디 닉네임 체크
        isUser = db.user.find_one({'id':id})
        if isUser is not None:
            return {'msg': 'exist id'}
        isNickName = db.user.find_one({'nickname': nickName})
        if isNickName is not None:
            return {'msg': 'exist nickname'}

        #DB에 user 추가 + pw 암호화 후 저장
        user = {
            'id': id,
            'pw': hashlib.sha256(pw.encode('utf8')).hexdigest(),
            'nickname': nickName
        }
        db.user.insert_one(user)

    except Exception as e:
        print(e)
        return {'msg': 'db error'}

    return {'msg': 'success'}



