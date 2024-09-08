from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class AuthApiSecret:
    def __init__(self):
        self.password_hasher = PasswordHasher()

    def generate(self, data: str) -> str:
        return self.password_hasher.hash(data)

    def verify(self, api_secret: str, data: str) -> bool:
        try:
            return self.password_hasher.verify(api_secret, data)
        except VerifyMismatchError:
            return False


auth_api_secret = AuthApiSecret()
