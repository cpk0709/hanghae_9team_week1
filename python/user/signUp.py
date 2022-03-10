import hashlib

from python.calendar.createCalendar import createCalendarProcess
from python.database.mongoDB import getConnection

#회원가입 프로세스
def signUpProcess(id, pwOne, pwTwo, nickName):

    client = getConnection()
    db = client.ourschedule

    try:
        #중복된 아이디 닉네임, 비밀번호 확인
        isUser = db.user.find_one({'id':id})
        if isUser is not None:
            return {'msg': 'exist id'}
        isNickName = db.user.find_one({'nickname': nickName})
        if isNickName is not None:
            return {'msg': 'exist nickname'}
        if pwOne != pwTwo:
            return {'msg': 'not equal password'}


        #DB에 user 추가 + pw 암호화 후 저장
        user = {
            'id': id,
            'pw': hashlib.sha256(pwOne.encode('utf8')).hexdigest(),
            'nickname': nickName
        }
        db.user.insert_one(user)

        #회원가입시 개인 캘린더 생성
        title = nickName + " 캘린더"
        re = createCalendarProcess(title, nickName)
        print(re)

    except Exception as e:
        print(e)
        return {'msg': 'db error'}

    return {'msg': 'success'}



