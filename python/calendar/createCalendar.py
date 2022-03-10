from python.database.mongoDB import getConnection


def createCalendarProcess(name, owner):
    #get db connection
    client = getConnection()
    db = client.ourschedule

    result = None
    try:
        #캘린더의 이름이 중복이면 만들지 않는다.
        if db.calendar.find_one({'name': name}) is not None:
            result = {'msg': 'exist name'}
        #존재하지 않는 user라면 만들지 않는다.
        elif db.user.find_one({'nickname': owner}) is None:
            result = {'msg': 'not exist nickname'}
        else:
            calendar = {
                'name': name,
                'owner': owner
            }
            db.calendar.insert_one(calendar)

            calendarId = db.calendar.find_one(calendar)['_id']
            userId = db.user.find_one({'nickname': owner})['_id']

            #user와 calendar의 다대다 관계를 위한 team table을 생성한다.
            team = {
                'userid': userId,
                'calendarid': calendarId
            }
            db.team.insert_one(team)

            result = {"calendarId": str(calendarId)}

    except Exception as e:
        print(e)
        result = {"msg": "db error"}

    return result

