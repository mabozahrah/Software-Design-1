from src.app import app


def test_profile_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = app

    
    with flask_app.test_client() as test_client:
        response = test_client.get('/profile')
        assert response.status_code == 302
        assert b"Redirecting" in response.data


def test_profile_page_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    flask_app = app

    
    with flask_app.test_client() as test_client:
        response = test_client.post('/profile')
        assert response.status_code == 302
        assert b"Login" not in response.data


def test_profile_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get('/profile')
    assert response.status_code == 302
    assert b"Redirecting" in response.data


def test_profile_page_post_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/profile')
    assert response.status_code == 302
    assert b"Login" not in response.data


def test_valid_profile(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is posted to (POST)
    THEN check the response is valid
    """
    response = test_client.post('/login',
                                data=dict(username='patkennedy79', password='password1'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for logging in, patkennedy79' in response.data
    assert b'History' in response.data
    assert b'Logout' in response.data

    response = test_client.post('/profile',
                                data=dict(name='John Doe', address1='4529 Marcus Street', city="Birmingham",
                                state="AL", zipcode="35203",user_id=1),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'History' in response.data
    assert b'Logout' in response.data