import pytest
from src.app import app, db, UserCredentials, ClientInformation, FuelQuote


@pytest.fixture(scope='module')
def new_user():
    user = UserCredentials('patkennedy79', 'password1')
    return user


@pytest.fixture(scope='module')
def new_profile():
    profile = ClientInformation(full_name='John Doe', address1='4529 Marcus Street', city="Birmingham",
                                state="AL", zipcode="352030", user_id=7)
    return profile


@pytest.fixture(scope='module')
def new_fuel_quote():
    fuel_quote = FuelQuote(gallons=7, delivery_date='2022-04-2', delivery_address='4529 Marcus Street', price=3.0,
                           user_id=7)
    return fuel_quote


@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    
    with flask_app.test_client() as testing_client:
        
        with flask_app.app_context():
            yield testing_client  


@pytest.fixture(scope='module')
def init_database(test_client):
    
    db.create_all()

    
    user1 = UserCredentials(username='patkennedy79', password_plaintext='password1')
    user2 = UserCredentials(username='kennedyfamilyrecipes', password_plaintext='password2')
    db.session.add(user1)
    db.session.add(user2)
    profile = ClientInformation(full_name='John Doe', address1='4529 Marcus Street', city="Birmingham",
                                state="AL", zipcode="352030", user_id=user1.id)

    db.session.add(profile)
    fuel_quote = FuelQuote(gallons=7, delivery_date='2022-04-2', delivery_address='4529 Marcus Street', price=3.0,
                           user=user1)

    db.session.add(fuel_quote)
    
    db.session.commit()

    yield  

    db.drop_all()


@pytest.fixture(scope='function')
def login_default_user(test_client):
    test_client.post('/login',
                     data=dict(username='patkennedy79', password='password1'),
                     follow_redirects=True)

    yield  

    test_client.get('/logout', follow_redirects=True)
