from model.model import UserModel,DetectModel

class UserController:
    @staticmethod
    def create_user(data):
        user_uuid, error = UserModel.create_user(data)
        if error:
            return None, error
        return {'message': 'User created successfully!', 'data': user_uuid}, None

    @staticmethod
    def login_user(data):
        user, error = UserModel.login_user(data)
        if error:
            return None, error
        return {'message': 'User login successfully!', 'data': user}, None

    @staticmethod
    def get_user(user_uuid):
        user, error = UserModel.get_user_by_uuid(user_uuid)
        if error:
            return None, error
        return {'message': 'Get User Data successfully!', 'data': user}, None

    @staticmethod
    def update_user(data):
        success, error = UserModel.update_user(data)
        if error:
            return None, error
        return {'message': 'User updated successfully!'}, None

    @staticmethod
    def delete_user(uuid):
        success, error = UserModel.delete_user(uuid)
        if error:
            return None, error
        return {'message': 'User deleted successfully!'}, None

class ModelController:
    @staticmethod
    def detect_phone(data):
        _data, error = DetectModel.detect_phone(data)
        if error:
            return None, error
        return {'message': 'Detect successfully!', 'data': _data}, None

    @staticmethod
    def upload_post(data):
        uploaded, error = DetectModel.upload_post(data)

        if error:
            return None, error

        return {'message': 'Upload successfully!'}, None

    @staticmethod
    def get_post():
        _data, error = DetectModel.get_post()
        if error:
            return None, error
        return {'message': 'Get Post Data successfully!', 'data': _data}, None

    @staticmethod
    def get_post_by_uuid(uuid):
        _data, error = DetectModel.get_post_by_uuid(uuid)
        if error:
            return None, error
        return {'message': 'Get Post Data successfully!', 'data': _data}, None