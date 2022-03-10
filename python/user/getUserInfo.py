from python.database.mongoDB import getConnection

def getUserInfoProcess(userId):
    client = getConnection()
    db = client.ourschedule

    try:
        # id로 DB에서 user 정보 가져오기(pw제외)
        userInfo = db.user.find_one({"id":userId}, {'pw': 0})

        return userInfo

    except Exception as e:
        print(e)
        return {"msg": "error"}

    client.close()