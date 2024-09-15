import pytest
from podcast.adapters import memory_repository
from podcast.adapters.memory_repository import MemoryRepository
from pathlib import Path
from podcast import create_app

# Using data from a different directory -- so we can test with fewer data
TEST_DATA_PATH = Path(__file__).parent / 'tests' / 'data'

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()

class AuthenticationManager:
    login_url = '/login'
    logout_url = '/logout'

    def __init__(self, client, default_name='TeamGoat', default_password='TeamGoat1!'):
        self.__client = client
        self.__default_name = default_name
        self.__default_password = default_password

    def login(self, user_name=None, password=None):
        if user_name is None:
            user_name = self.__default_name
        if password is None:
            password = self.__default_password

        return self.__client.post(
            self.login_url,
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get(self.logout_url)


@pytest.fixture
def auth(client):
    # creates an authentication instance with the client
    return AuthenticationManager(client)
