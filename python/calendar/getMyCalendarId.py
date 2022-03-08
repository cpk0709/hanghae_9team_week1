from python.database.mongoDB import getConnection
from bson import ObjectId

def getMyCalendarIdProcess(calendarIdList, nickname):
    client = getConnection()
    db = client.ourschedule

    try:
        calendarId = ''
        for cal in calendarIdList:
            print(cal)
            myCalendarId = db.calendar.find_one({'_id': ObjectId(cal['calendarid']), 'name': nickname + ' 캘린더'})
            if myCalendarId is not None:
                calendarId = str(myCalendarId['_id'])

        return calendarId

    except Exception as e:
        print(e)
        return {"msg": "error"}