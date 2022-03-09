from bson import ObjectId

from python.database.mongoDB import getConnection


def deletePostProcess(postId):
    # get db connection
    client = getConnection()
    db = client.ourschedule

    result = None
    try:
        if db.post.find_one({'_id': ObjectId(postId)}) is None:
            result = {'msg': 'not exist post'}
        else:
            db.post.delete_one({'_id': ObjectId(postId)})
            result = {'msg': 'success'}
    except Exception as e:
        print(e)
        result = {'msg': 'db error'}

    return result