from python.database.mongoDB import getConnection

def newCalendar(name, owner):
    result = ""

    client = getConnection()
    db = client.ourschedule
    try:

        if db.calendar.find_one({'name': name}) is not None:
            return {'msg': 'exist name'}


        calendar = {
            'name': name,
            'owner': owner
        }
        db.calendar.insert_one(calendar)

        calendarId = db.calendar.find_one(calendar)['_id']
        userId = db.user.find_one({'nickname': owner})['_id']

        print(calendarId, userId)

        team = {
            'userid': userId,
            'calendarid': calendarId
        }
        db.team.insert_one(team)

        return {"calendarId": str(calendarId)}

    except Exception as e:
        print(e)
        return {"msg": "db error"}

    return result

