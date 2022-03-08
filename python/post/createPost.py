from python.database.mongoDB import getConnection


def createPostProcess(calendarId, dateTime, content, nickname):
    #get db connection
    client = getConnection()
    db = client.ourschedule

    try:
        post = {
            'calendarId': calendarId,
            'datatime':dateTime,
            'content': content,
            'nickname': nickname
        }

        db.post.insert_one(post)

        postId = db.post.find_one(post)['_id']

        result = {'postId': str(postId)}


    except Exception as e:
        print(e)
        result = {'msg': 'db error'}

    return result