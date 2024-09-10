from werkzeug.security import generate_password_hash, check_password_hash
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User

def add_user(username: str, password: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user != None:
        return Exception('User already exists')

    pass_encrypted = generate_password_hash(password)
    user = User(user_id=hash(username), username=username, password=pass_encrypted)
    repo.add_user(user)

def get_user(username: str, repo: AbstractRepository):
    user = repo.get_user(username)
    if user == None:
        return Exception("User not found or User does not exist!")

    return user


def authenticate_user(username: str, password: str, repo: AbstractRepository):
    auth = False

    user = repo.get_user(username)
    if User != None:
        auth = check_password_hash(user.password, password)
    if auth == False:
        return Exception("Authentication Failed!")
