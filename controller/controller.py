from model.model import UserModel

class UserController:
    @staticmethod
    def create_user(data):
        user_uuid, error = UserModel.create_user(data)
        if error:
            return None, error
        return {'message': 'User created successfully!', 'uuid': user_uuid}, None

    @staticmethod
    def login_user(data):
        user, error = UserModel.login_user(data)
        if error:
            return None, error
        return {'message': 'User login successfully!', 'user': user}, None

    @staticmethod
    def get_user(user_uuid):
        user, error = UserModel.get_user_by_uuid(user_uuid)
        if error:
            return None, error
        return user, None

    @staticmethod
    def update_user(user_uuid, data):
        success, error = UserModel.update_user(user_uuid, data)
        if error:
            return None, error
        return {'message': 'User updated successfully!'}, None

    @staticmethod
    def delete_user(user_uuid):
        success, error = UserModel.delete_user(user_uuid)
        if error:
            return None, error
        return {'message': 'User deleted successfully!'}, None
