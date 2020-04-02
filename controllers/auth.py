from controllers.base import BaseController
from controllers.mixins import LoginMixin


class LoginBaseController(BaseController, LoginMixin):
    def authenticate(self):
        pass


class RegisterBaseController(BaseController, LoginMixin):
    def get_password_digest(self):
        pass


class LogoutBaseController(BaseController):
    def logout(self):
        pass
