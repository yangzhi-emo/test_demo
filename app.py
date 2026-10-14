from flask import Flask, request, jsonify

app = Flask(__name__)

# 模拟测试账号
TOKEN = "test-token-123"


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    if data.get("username") == "test" and data.get("password") == "123456":
        return jsonify({
            "code": 200,
            "message": "登录成功",
            "token": TOKEN
        }), 200

    return jsonify({
        "code": 401,
        "message": "用户名或密码错误"
    }), 401


@app.route("/user", methods=["GET"])
def get_user():
    token = request.headers.get("Authorization")

    if token != f"Bearer {TOKEN}":
        return jsonify({
            "code": 401,
            "message": "未授权"
        }), 401

    return jsonify({
        "code": 200,
        "data": {
            "id": 1,
            "username": "test"
        }
    }), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)