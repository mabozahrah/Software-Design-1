#Brooke
def test_login_page(test_client):
    
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Username' in response.data
    assert b'Password' in response.data


def test_valid_login_logout(test_client, init_database):
    
    response = test_client.post('/login',
                                data=dict(username='patkennedy79', password='password1'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for logging in, patkennedy79' in response.data
    assert b'History' in response.data
    assert b'Logout' in response.data


    
    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' not in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data


def test_invalid_login(test_client, init_database):
    
    response = test_client.post('/login',
                                data=dict(username='patkennedy79', password='password111'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Logout' not in response.data
    assert b'Login' in response.data
    assert b'Register' in response.data


def test_login_already_logged_in(test_client, init_database, login_default_user):
    
    response = test_client.post('/login',
                                data=dict(username='patkennedy79', password='FlaskIsNotAwesome'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Already logged in!' in response.data
    assert b'Logout' in response.data
    assert b'Login' not in response.data
    assert b'Register' not in response.data


def test_valid_registration(test_client, init_database):
    
    response = test_client.post('/register',
                                data=dict(username='patkennedy99',
                                          password='FlaskIsGreat'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering' in response.data


def test_duplicate_registration(test_client, init_database):
    
    
    test_client.post('/register',
                     data=dict(username='pkennedy@hey.com',
                               password='FlaskIsTheBest'),
                     follow_redirects=True)
    
    response = test_client.post('/register',
                                data=dict(username='pkennedy@hey.com',
                                            password='FlaskIsTheBest'),
                                follow_redirects=True)
    assert response.status_code == 200
    assert b'Thanks for registering, pkennedy@hey.com!' not in response.data

