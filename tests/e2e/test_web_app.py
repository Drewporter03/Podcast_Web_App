from tests.conftest import client


# Test that the home page returns the welcome message
def test_home(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b'<h1>Welcome to <a href="home"><span class="logo">mixcast.<'b'/span></a></h1>' in response.data


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
