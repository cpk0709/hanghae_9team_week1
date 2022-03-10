from python.database.mongoDB import getConnection

#db에서 userId를 통해 user정보를 찾아내는 함수
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

