from bson import ObjectId

from python.database.mongoDB import getConnection

def getCalendarProcess(calendarId):
    # get db connection
    client = getConnection()
    db = client.ourschedule

    try:
        result = []

        #calander id 에 해당하는 post 리스트를 만든다.
        calendar = db.post.find({'calendarId': ObjectId(calendarId)})
        for sub in calendar:
            print(sub)
            sub['_id'] = str(sub['_id'])
            result.append(sub)

        # post가 없다면 none을 반환한다.
        if len(result) == 0:
            result = "none"

        result = {"schedule": result}

    except Exception as e:
        print(e)
        result = {'msg': "db error"}


    return result


# mocking 데이터 생성 함수
def mockdata():
    client = getConnection()
    db = client.ourschedule

    doc1 = {
        "date": 'dateTime',
        "time": 'Time',
        "content": 'Content',
        "nickname": "woong",
        "calendarid": ObjectId('11')
    }
    doc2 = {
        "date": '1',
        "time": '32',
        "content": 'Content',
        "nickname": "woong",
        "calendarid": ObjectId('11'),
    }
    db.calendar.insert_one(doc1)
    db.calendar.insert_one(doc2)

    return
