from flask import Blueprint, request, jsonify
from controller.controller import UserController, ModelController
app_route = Blueprint("user", __name__)

# 사용자 생성
@app_route.route("/user/create", methods=["POST"])
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
@app_route.route("/user/login", methods=["POST"])
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
@app_route.route("/user/read/<uuid>", methods=["GET"])
def read_user(uuid):
    response, error = UserController.get_user(uuid)
    if error:
        return jsonify({"message": error, "status": 404}), 404
    return jsonify({**response, "status": 200}), 200

# 사용자 정보 수정
@app_route.route("/user/update", methods=["PUT"])
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
@app_route.route("/user/delete/<uuid>", methods=["DELETE"])
def delete_user(uuid):
    response, error = UserController.delete_user(uuid)
    if error:
        return jsonify({"message": error, "status": 404}), 404

    return jsonify({**response, "status": 200}), 200

@app_route.route("/detect/detect", methods=["POST"])
def detect_objects():
    image_data = request.data
    if not image_data:
        return jsonify({"message": f"image is required!", "status": 404}), 400

    response, error = ModelController.detect_phone(image_data)
    if error:
        return jsonify({"message": error, "status": 404}), 404

    return jsonify({**response, "status": 200}), 200

@app_route.route("/detect/upload", methods=["POST"])
def upload_post():
    data = request.get_json()
    required_fields = ["uuid", "subject", "start_time", "end_time", "waste_time"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"{field.capitalize()} is required!", "status": 404}), 400

    response, error = ModelController.upload_post(data)
    if error:
        return jsonify({"message": error, "status": 404}), 404

    return jsonify({**response, "status": 200}), 200

@app_route.route("/detect/read", methods=["GET"])
def read_post():
    response, error = ModelController.get_post()
    if error:
        return jsonify({"message": error, "status": 404}), 404
    return jsonify({**response, "status": 200}), 200

@app_route.route("/detect/read/<uuid>", methods=["GET"])
def read_post_by_uuid(uuid: str):
    response, error = ModelController.get_post_by_uuid(uuid)
    if error:
        return jsonify({"message": error, "status": 404}), 404

    return jsonify({**response, "status": 200}), 200