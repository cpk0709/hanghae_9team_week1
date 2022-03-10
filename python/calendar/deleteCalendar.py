from bson import ObjectId

from python.database.mongoDB import getConnection

def deleteCalendarProcess(calendarId):
    #get db connection
    client = getConnection()
    db = client.ourschedule

    result = None
    try:
            # 캘린더id 와 매칭되는 캘린더가 없으면 실행하지 않는다.
        if db.calendar.find_one({'_id': ObjectId(calendarId)}) is None:
            result = {'msg': 'not exist calendar id'}
        else:
            # 캘린더를 지우는 동시에 캘린더와 연관된 team, post를 모두 지운다
            db.team.delete_many({'calendarid': ObjectId(calendarId)})
            db.post.delete_many({'calendarid': calendarId})
            db.calendar.delete_one({'_id': ObjectId(calendarId)})

            result = {'msg': 'success'}

    except Exception as e:
        print(e)
        result = {'msg': 'db error'}

    return result
