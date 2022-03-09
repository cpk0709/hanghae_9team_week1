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
        calendar = list(db.calendar.find({}))
        user = list(db.user.find({}))
        team = list(db.team.find({}))
        print(calendar)
        print(user)
        print(team)

        userInfo = db.user.find_one({'id': id})
        if userInfo is not None:
            _id = userInfo['_id']
            nickname = userInfo['nickname']
        else:
            return {"msg": "ID is not existed"}

        # calendarList = list(db.team.find({'userid': ObjectId(_id)}, {'_id': 0, 'userid': 0})) # ObjectId타입
        MyCalendar = db.calendar.find_one({'owner': nickname, 'name':nickname+' 캘린더'})

        CalendarList = list(db.calendar.find({'owner': nickname}))

        personal = {}
        team = {}
        teamList = []
        for cal in CalendarList:
            if cal['name'] == nickname+' 캘린더':
                personal['_id'] = str(cal['_id'])
                personal['name'] = cal['name']
            else:
                teamEach = {}
                teamEach['_id'] = str(cal['_id'])
                teamEach['name'] = cal['name']
                teamList.append(teamEach)
                team['list'] = teamList
        result['personal'] = personal
        result['team'] = team

        return result

    except Exception as e:
        print(e)
        return {"msg": "error"}