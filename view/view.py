from flask import Blueprint, request, jsonify
from controller.controller import UserController
app_route = Blueprint("user", __name__)

# 사용자 생성
@app_route.route("/create", methods=["POST"])
def create_user():
    data = request.get_json()

    required_fields = ["email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"{field.capitalize()} is required!", "status": 404}), 400

    response, error = UserController.create_user(data)
    if error:
        return jsonify({"message": error, "status": 404}), 404 if "exists" in error else 500

    return jsonify({**response, "status": 200}), 201

# 로그인
@app_route.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()

    required_fields = ["email", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"{field.capitalize()} is required!"}), 400

    response, error = UserController.login_user(data)

    if error:
        return jsonify({"message": error, "status": 404}), 404
    return jsonify({**response, "status": 200}), 200

# 사용자 정보 조회
@app_route.route("/read/<uuid>", methods=["GET"])
def read_user(uuid):
    response, error = UserController.get_user(uuid)
    if error:
        return jsonify({"message": error, "status": 404}), 404
    return jsonify({**response, "status": 200}), 200

# 사용자 정보 수정
@app_route.route("/update", methods=["PUT"])
def update_user():
    data = request.get_json()

    required_fields = ["uuid", "password"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"{field.capitalize()} is required!", "status": 404}), 400

    response, error = UserController.update_user(data)
    if error:
        return jsonify({"message": error, "status": 404}), 404

    return jsonify({**response, "status": 200}), 200

# 사용자 삭제
@app_route.route("/delete/<uuid>", methods=["DELETE"])
def delete_user(uuid):
    response, error = UserController.delete_user(uuid)
    if error:
        return jsonify({"message": error, "status": 404}), 404

    return jsonify({**response, "status": 200}), 200


# app_route = Blueprint("user", __name__)
#
#
# @app_route.route("/create", methods=["POST"])
# def create_user():
#     data = request.get_json()
#
#     required_fields = ["email", "password"]
#     for field in required_fields:
#         if field not in data or not data[field]:
#             return jsonify({"message": f"{field.capitalize()} is required!","status": 404}), 400
#
#     response, error = UserController.create_user(data)
#     if error:
#         return jsonify({"message": error,"status": 404}), 404 if "exists" in error else 500
#
#     return jsonify(response + {"status": 200}), 201
#
#
# @app_route.route("/login", methods=["POST"])
# def login_user():
#     data = request.get_json()
#
#     required_fields = ["email", "password"]
#     for field in required_fields:
#         if field not in data or not data[field]:
#             return jsonify({"message": f"{field.capitalize()} is required!"}), 400
#
#     response, error = UserController.login_user(data)
#
#     if error:
#         return jsonify({"message": error,"status": 404}), 404
#     return jsonify(response + {"status": 200}), 200
#
#
# @app_route.route("/read/<uuid>", methods=["GET"])
# def read_user(uuid):
#     response, error = UserController.get_user(uuid)
#     if error:
#         return jsonify({"message": error,"status": 404}), 404
#     return jsonify(response + {"status": 201}), 200
#
#
# @app_route.route("/update/<uuid>", methods=["PUT"])
# def update_user(uuid):
#     data = request.get_json()
#
#     required_fields = ["email", "password"]
#     for field in required_fields:
#         if field not in data or not data[field]:
#             return jsonify({"message": f"{field.capitalize()} is required!","status": 404}), 400
#
#     response, error = UserController.update_user(uuid, data)
#     if error:
#         return jsonify({"message": error,"status": 404}), 404
#
#     return jsonify(response + {"status": 201}), 200
#
#
# @app_route.route("/delete/<uuid>", methods=["DELETE"])
# def delete_user(uuid):
#     response, error = UserController.delete_user(uuid)
#     if error:
#         return jsonify({"message": error,"status": 404}), 404
#
#     return jsonify(response + {"status": 201}), 200
#
#
# from flask import Blueprint, request, jsonify
# from controller.controller import UserController
#