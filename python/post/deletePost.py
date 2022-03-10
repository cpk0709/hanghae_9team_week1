from bson import ObjectId
from python.database.mongoDB import getConnection

#포스트를 삭제하는 서비스
def deletePostProcess(postId):
    # get db connection
    client = getConnection()
    db = client.ourschedule

    result = None
    try:
        #포스트가 없다면
        if db.post.find_one({'_id': ObjectId(postId)}) is None:
            result = {'msg': 'not exist post'}
        else:
            db.post.delete_one({'_id': ObjectId(postId)})
            result = {'msg': 'success'}
    except Exception as e:
        print(e)
        result = {'msg': 'db error'}

    return result
