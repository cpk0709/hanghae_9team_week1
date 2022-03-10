from python.database.mongoDB import getConnection
import pymongo
from bson import ObjectId

def editPostProcess(calendarId, dateTime, content, postId):
    client = getConnection()
    db = client.ourschedule
    result = {}
    try:

        # dbResult = db.post.update_one({'_id': postId},
        dbResult = db.post.update_one({'_id':  ObjectId(postId)},
                           {'$set': {'datatime': dateTime, 'content': content }})
        print(dbResult)
        print(dbResult.matched_count > 0)

        if dbResult.matched_count>0:
            result = {'postId': 'post edit is success'}


        post = list(db.post.find({}))
        print(post)




    except Exception as e:
        print(e)
        result = {'msg': 'db error'}

    return result