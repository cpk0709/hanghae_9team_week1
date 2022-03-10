from python.database.mongoDB import getConnection
from bson import ObjectId

def getMyCalendarIdProcess(calendarIdList, nickname):
    client = getConnection()
    db = client.ourschedule

    try:
        calendarId = ''
        for cal in calendarIdList:
            myCalendarId = db.calendar.find_one({'_id': ObjectId(cal['calendarid']), 'name': nickname + ' 캘린더'})
            if myCalendarId is not None:
                calendarId = str(myCalendarId['_id'])

        return calendarId

    except Exception as e:
        print(e)
        return {"msg": "error"}

    client.close()

def getMyCalendarIdProcess2(nickname):
    client = getConnection()
    db = client.ourschedule

    try:
        calendarId = ''
        myCalendar = db.calendar.find_one({'name': nickname + ' 캘린더'})

        if myCalendar is not None:
            calendarId = str(myCalendar['_id'])

        return calendarId

    except Exception as e:
        print(e)
        return {"msg": "error"}

    client.close()