from python.database.mongoDB import getConnection
from bson import ObjectId

def getCalendarIdListProcess(_id): # 캘린더ID리스트만(기존버전)
    client = getConnection()
    db = client.ourschedule

    try:
        # calendarIds = list(db.team.find({'userid': _id}, {'_id': 0, 'userid': 0}))            # String타입
        calendarIdList = list(db.team.find({'userid': ObjectId(_id)}, {'_id': 0, 'userid': 0})) # ObjectId타입
        print(calendarIdList)
        # calendarIdList = dict(db.team.find({'userid': ObjectId(_id)}, {'_id': 0, 'userid': 0}))

        return calendarIdList

    except Exception as e:
        print(e)
        return {"msg": "error"}

def getCalendarListProcess(id): #캘린더 개인/팀 - 캘린더ID/이름
    client = getConnection()
    db = client.ourschedule

    result = {}

    try:
        userInfo = db.user.find_one({'id': id})
        _id = userInfo['_id']
        nickname = userInfo['nickname']

        # calendarList = list(db.team.find({'userid': ObjectId(_id)}, {'_id': 0, 'userid': 0})) # ObjectId타입
        MyCalendar = db.calendar.find_one({'owner': nickname, 'name':nickname+' 캘린더'})
        MyCalendarId = str(MyCalendar['_id'])
        personal = {}
        # personal['_id'] = MyCalendarId
        # personal['name'] = MyCalendar['name']
        # print('personal:', personal)

        # TeamCalendarList = list(db.team.find({'userid': ObjectId(_id)}, {'_id': 0, 'userid': 0}))
        CalendarList = list(db.calendar.find({'owner': nickname}))
        print(CalendarList)

        team = {}
        teamList = []
        for cal in CalendarList:
            # calenarInfo = db.calendar.find_one({'_id': ObjectId(i['calendarid'])})
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
        print(result)

        return result

    except Exception as e:
        print(e)
        return {"msg": "error"}