from src.app import app


def test_fuel_quote_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = app

    
    with flask_app.test_client() as test_client:
        response = test_client.get('/fuel-quote')
        assert response.status_code == 302
        assert b"Redirecting" in response.data


def test_fuel_quote_page_post():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    flask_app = app

    
    with flask_app.test_client() as test_client:
        response = test_client.post('/fuel-quote')
        assert response.status_code == 302
        assert b"Login" not in response.data




def test_fuel_quote_post_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is is posted to (POST)
    THEN check that a '405' status code is returned
    """
    response = test_client.post('/profile')
    assert response.status_code == 302
    assert b"Login" not in response.data


def test_valid_fuel_quote(test_client, init_database):
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

    response = test_client.post('/fuel-quote',
                                data=dict(gallons=7, delivery_date='2022-04-2', delivery_address='4529 Marcus Street',
                                          price=3.0, user_id=1),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'History' in response.data
    assert b'Logout' in response.data