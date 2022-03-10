from python.database.mongoDB import getConnection


def editPostProcess(calendarId, dateTime, content, postId):
    client = getConnection()
    db = client.ourschedule

    try:
        post = {
            'calendarId': calendarId,
            'datatime':dateTime,
            'content': content,
            'postId': postId
        }

        db.post.insert_one(post)

        db.post.update_one({'calendarId': calendarId},
                           {'$set': {'datatime': dateTime, 'content': content, 'postId': postId} })

        result = {'postId': 'post edit is success'}



    except Exception as e:
        print(e)
        result = {'msg': 'db error'}

    return result