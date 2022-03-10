from bson import ObjectId

from python.database.mongoDB import getConnection

def getCalendarProcess(calendarId):
    # get db connection
    client = getConnection()
    db = client.ourschedule

    try:
        result = []

        #calander id 에 해당하는 post 리스트를 만든다.
        calendar = db.post.find({'calendarId': calendarId})
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
