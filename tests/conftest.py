import pytest
from podcast.adapters import memory_repository
from podcast.adapters.memory_repository import MemoryRepository, populate
from pathlib import Path
from podcast import create_app

TEST_DATA_PATH = Path(__file__).parent / 'adapters' / 'data'
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