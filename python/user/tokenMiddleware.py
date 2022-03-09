from functools import wraps
import jwt
from flask import request, render_template, make_response, jsonify, Response
from python.user.tokenCheck import tokenCheckProcess
from flask import current_app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "myToken" in request.cookies:
            token = request.cookies.get('myToken')
            tokenMsg = tokenCheckProcess(token)
            if token is not None:
                if tokenMsg['result'] == 'success':
                    id = tokenMsg['id']

                elif tokenMsg['result'] == 'fail' and tokenMsg['msg'] == '로그인 시간이 만료되었습니다.':
                    return {'message':'로그인 시간이 만료되었습니다.'}

                elif tokenMsg['result'] == 'fail' and tokenMsg['msg'] == '로그인 정보가 존재하지 않습니다.':
                    return {'message':'로그인 정보가 존재하지 않습니다.'}
            else:
                return{'message':'로그인해주세요.'}
        else:
            return { "message": "로그인해주세요."}, 401
            # return render_template('signin.html')
            # return make_response("Token is missing", 401, )
            # return make_response(jsonify({"message": "Token is missing!"}), 401)
            # return Response(status = 401)
        # try:
        #     data=jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        #     current_user=models.User().get_by_id(data["user_id"])
        #     if current_user is None:
        #         return {
        #         "message": "Invalid Authentication token!",
        #         "data": None,
        #         "error": "Unauthorized"
        #     }, 401
        #     if not current_user["active"]:
        #         abort(403)
        # except Exception as e:
        #     return {
        #         "message": "Something went wrong",
        #         "data": None,
        #         "error": str(e)
        #     }, 500

        # return f(id, *args, **kwargs)
        return f(*args, **kwargs)

    return decorated