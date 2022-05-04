from src.app import app

#Mariam
def test_home_page():
    
    flask_app = app

    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 302
        assert b"Redirecting" in response.data



def test_home_page_post():
    
    flask_app = app

    with flask_app.test_client() as test_client:
        response = test_client.post('/')
        assert response.status_code == 405
        assert b"Login" not in response.data


def test_home_page_with_fixture(test_client):
    
    response = test_client.get('/')
    assert response.status_code == 302
    assert b"Redirecting" in response.data



def test_home_page_post_with_fixture(test_client):
    
    response = test_client.post('/')
    assert response.status_code == 405
    assert b"Login" not in response.data



def test_valid_home_page(test_client, init_database):
    
    response = test_client.post('/login',
                                data=dict(username='patkennedy79', password='password1'),
                                follow_redirects=True)

    assert response.status_code == 200
    assert b'Thanks for logging in, patkennedy79' in response.data
    assert b'History' in response.data
    assert b'Logout' in response.data

