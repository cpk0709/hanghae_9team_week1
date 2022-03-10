from python.database.mongoDB import getConnection
from bson import ObjectId

#포스트를 수정하는 서비스
def editPostProcess(calendarId, dateTime, content, postId):
    client = getConnection()
    db = client.ourschedule

    result = {}
    try:
        post = {
            'calendarId': calendarId,
            'datatime':dateTime,
            'content': content,
            'postId': postId
        }

        dbResult = db.post.update_one({'_id':  ObjectId(postId)}, {'$set': {'datatime': dateTime, 'content': content}})

        #성공적으로 수정 되었다면
        if dbResult.matched_count>0:
            result = {'postId': 'post edit is success'}

    except Exception as e:
        print(e)
        result = {'msg': 'db error'}

    return result