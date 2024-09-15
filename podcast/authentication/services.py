from werkzeug.security import generate_password_hash, check_password_hash
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User


class NameNotUniqueException(Exception):
    pass
class UnknownUserException(Exception):
    pass
class AuthenticationException(Exception):
    pass


def add_user(username: str, password: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user != None:
        raise NameNotUniqueException

    pass_encrypted = generate_password_hash(password)
    # hashing user Id
    h = hash(username)
    # user id cant be a negative number hence if it is it inverses to a positive.
    if h < 0:
        h *= -1
    user = User(user_id=h, username=username, password=pass_encrypted)
    repo.add_user(user)


def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    print(f"Adding user with username: {user}")
    if user == None:

        raise UnknownUserException

    return user


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    auth = False

    user = repo.get_user(username)
    if user != None:
        auth = check_password_hash(user.password, password)
    if auth == False:
        raise AuthenticationException
