from python.database.mongoDB import getConnection
from bson import ObjectId

def getCalendarIdListProcess(_id): # 캘린더ID리스트만(기존버전)
    client = getConnection()
    db = client.ourschedule

    try:
        # calendarIds = list(db.team.find({'userid': _id}, {'_id': 0, 'userid': 0}))            # String타입
        calendarIdList = list(db.team.find({'userid': ObjectId(_id)}, {'_id': 0, 'userid': 0})) # ObjectId타입
        # calendarIdList = dict(db.team.find({'userid': ObjectId(_id)}, {'_id': 0, 'userid': 0}))

        return calendarIdList

    except Exception as e:
        print(e)
        return {"msg": "error"}

def getCalendarListProcess(id): #캘린더 개인,팀 - 캘린더ID/이름
    client = getConnection()
    db = client.ourschedule

    result = {}

    try:
        userInfo = db.user.find_one({'id': id})
        if userInfo is not None:
            _id = userInfo['_id']
            nickname = userInfo['nickname']
        else:
            return {"msg": "ID is not existed"}

        teamCalendarList = list(db.team.find({'userid': ObjectId(_id)}, {'_id': 0, 'userid': 0})) # ObjectId타입

        CalendarList = list(db.calendar.find({'owner': nickname})) #개인, 내가 만든 캘린더

        personal = {}
        team = {}
        teamList = []
        myOwnCalendar = [] # 내가 소유한 캘린더 ID리스트
        for cal in CalendarList:
            # 내 개인 캘린더
            if cal['name'] == nickname+' 캘린더':
                personal['_id'] = str(cal['_id'])
                personal['name'] = cal['name']
            # 개인캘린더 외에 내가 소유한 캘린더 ---- 없을때
            else:
                teamEach = {}
                teamEach['_id'] = str(cal['_id'])
                teamEach['name'] = cal['name']
                teamList.append(teamEach)
                # team['list'] = teamList
            myOwnCalendar.append(str(cal['_id']))
        for cal in teamCalendarList:
            # 팀캘린더에 있는데 내소유 캘린더 아닌 것(공유캘린더)을 뒤에 추가
            if str(cal['calendarid']) not in myOwnCalendar:
                ourCalendar = db.calendar.find_one({'_id': cal['calendarid']})
                teamEach = {}
                teamEach['_id'] = str(ourCalendar['_id'])
                teamEach['name'] = ourCalendar['name']
                teamList.append(teamEach)
        team['list'] = teamList
        result['personal'] = personal
        result['team'] = team

        return result

    except Exception as e:
        print(e)
        return {"msg": "error"}