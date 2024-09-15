from tests.conftest import client
import pytest
from flask import session


# Test that the home page returns the welcome message
def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200

    assert b'<h1>Welcome to <a href="home" class="highlight logo">mixcast.</a></h1>' in response.data


# Test that the podcasts page returns the header 'Podcasts' and the first episode "#better"
def test_podcasts_page(client):
    response = client.get('/podcasts')
    assert response.status_code == 200
    assert b'Podcasts' in response.data
    assert b'#better' in response.data


# Test the episodes page returns the correct episodes based on the podcast_id
def test_episodes_page(client):
    response = client.get('/episodes?podcast_id=5')
    assert response.status_code == 200
    assert b'Bethel Presbyterian Church (EPC) Sermons' in response.data
    assert b'Believing the Impossible (Luke 1:26-45)' in response.data


# Tests the register page works as intended
def test_register_page(client):
    response = client.get('/register').status_code
    assert response == 200
    response_data = client.post('/register', data={
        'user_name': 'kumanan', 'password': 'BigManTing1'})
    assert response_data.headers['Location'] == '/login'

# Tests the register page works as intended when an unusable password is used
def test_register_page_failed_only_numbers(client,):
    response_data = client.post('/register', data={
        'user_name': 'kumanan', 'password': '111111111111'})
    message = b"Password must contain at least one upper case letter, one lower case and at least one digit."
    assert message in response_data.data

# Tests the register page works as intended when an unusable password is used
def test_register_page_failed_only_letters(client,):
    response_data = client.post('/register', data={
        'user_name': 'kumanan', 'password': 'aaaaaaaaaaaa'})
    message = b"Password must contain at least one upper case letter, one lower case and at least one digit."
    assert message in response_data.data

