from python.database.mongoDB import getConnection

def getMyCalendarIdProcess2(nickname):
    client = getConnection()
    db = client.ourschedule

    try:
        calendarId = ''
        #개인 캘린더인 문자열을 찾아 db에서 조회
        myCalendar = db.calendar.find_one({'name': nickname + ' 캘린더'})

        if myCalendar is not None:
            calendarId = str(myCalendar['_id'])
        else:
            return{'msg':'no calendar'}

        return calendarId

    except Exception as e:
        print(e)
        return {"msg": "error"}

