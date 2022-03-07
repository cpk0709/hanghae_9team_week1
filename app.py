from flask import Flask, render_template, request, jsonify
from python.user.signUp import signUpProcess

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/user/signUp', methods=["POST"])
def signUp():
    user = request.get_json()

    msg = signUpProcess(user['id'], user['pw'], user['nickName'])
    return jsonify(msg)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

