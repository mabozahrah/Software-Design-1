from src.app import app
import json
#Brooke
def test_fuel_quote_page():
    
    flask_app = app

    with flask_app.test_client() as test_client:
        response = test_client.get('/fuel-quote')
        assert response.status_code == 302
        assert b"Redirecting" in response.data


def test_get_quote_page_post():
    
    flask_app = app

    with flask_app.test_client() as test_client:
        response = test_client.post('/fuel-quote')
        assert response.status_code == 302
        assert b"Login" not in response.data




def test_get_quote_post_with_fixture(test_client):
    
    response = test_client.post('/get-quote')
    assert response.status_code == 302
    assert b"Login" not in response.data


def test_valid_get_quote(test_client, init_database):
    
    response = test_client.post('/login',
                                data=dict(username='patkennedy79', password='password1'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'Thanks for logging in, patkennedy79' in response.data
    assert b'History' in response.data
    assert b'Logout' in response.data


    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    response = test_client.post('/get-quote',
                                json={"gallons": 1000, 'state': 'TX'},
                                )

    assert response.get_json()['suggested_price'] == 1.71
    assert response.get_json()['total_amount'] == 1710.0
