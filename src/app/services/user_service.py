from src.app.repositories.user_repository import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int):

        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise Exception("User not found")

        return user

    def update_profile(self, user_id: int, data):

        user = self.user_repository.get_by_id(user_id)

        if not user:
            raise Exception("User not found")

        user.fullname = data.fullname
        user.avatar = data.avatar

        return self.user_repository.update(user)
