from python.database.mongoDB import getConnection


def updatePostProcess():
    # get db connection
    client = getConnection()
    db = client.ourschedule


    return