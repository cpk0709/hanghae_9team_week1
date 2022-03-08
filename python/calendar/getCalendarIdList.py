from python.database.mongoDB import getConnection
from bson import ObjectId

def getCalendarIdListProcess(_id):
    client = getConnection()
    db = client.ourschedule

    try:
        # calendarIds = list(db.team.find({'userid': _id}, {'_id': 0, 'userid': 0}))         # String타입
        calendarIdList = list(db.team.find({'userid': ObjectId(_id)}, {'_id': 0, 'userid': 0})) # ObjectId타입

        return calendarIdList

    except Exception as e:
        print(e)
        return {"msg": "error"}