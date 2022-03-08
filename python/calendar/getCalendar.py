from python.database.mongoDB import getConnection

def getCalendar(calendarId):
    client = getConnection()
    db = client.ourschedule

    try:
        calendar = db.post.find({'calendarId': 111})

        result = []
        for sub in calendar:
            print(sub)
            sub['_id'] = str(sub['_id'])
            result.append(sub)

    except Exception as e:
        print(e)
        return {'msg': "db error"}

    if len(result) == 0:
        result = "none"

    return {"schedule": result}

def dummydata():
    client = getConnection()
    db = client.ourschedule

    doc1 = {
        "date": 'dateTime',
        "time": 'Time',
        "content": 'Content',
        "nickname": "woong",
        "calendarid": '11'
    }
    doc2 = {
        "date": '1',
        "time": '32',
        "content": 'Content',
        "nickname": "woong",
        "calendarid": '11',
    }
    db.calendar.insert_one(doc1)
    db.calendar.insert_one(doc2)

    return
