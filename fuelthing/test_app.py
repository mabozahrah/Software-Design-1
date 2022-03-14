import pytest
from app import app

"""---------- coverage: platform linux, python 3.8.10-final-0 -----------
Name          Stmts   Miss  Cover
---------------------------------
test_app.py      75      0   100%
---------------------------------
TOTAL            75      0   100%
"""

#All of us worked on this together
class TestLogin:

    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_get_login(self, client):
        resp = client.get('/login')
        assert resp.status_code == 200

    def test_login_with_correct_data(self, client):
        response = client.post("/login", data={
            "username": "admin",
            "password": "secret-password"
        })
        assert response.status_code == 200
        assert response.json.get('success')

    def test_login_with_fake_data(self, client):
        resp = client.post('/login', data={
            "username": "user",
            "password": "password"
        })
        assert resp.status_code == 400
        assert not resp.json.get('success')


class TestProfile:

    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_get_profile(self, client):
        resp = client.get('/profile')
        assert resp.status_code == 200

    def test_correct_form(self, client):
        response = client.post("/profile", data={
            "name": "admin",
            "address1": "3646 Bates Brothers Road",
            "address2": "3646 Bates Brothers Road",
            "city": "Columbus",
            "state": "Ohio",
            "zipcode": "43215"
        })
        assert response.status_code == 200
        assert response.json.get('success')

    def test_data_without_optional(self, client):
        response = client.post("/profile", data={
            "name": "admin",
            "address1": "3646 Bates Brothers Road",
            "address2": "",
            "city": "Columbus",
            "state": "Ohio",
            "zipcode": "43215"
        })
        assert response.status_code == 200
        assert response.json.get('success')

    def test_name_required_field(self, client):
        response = client.post("/profile", data={
            "name": "",
            "address1": "3646 Bates Brothers Road",
            "address2": "3646 Bates Brothers Road",
            "city": "Columbus",
            "state": "Ohio",
            "zipcode": "43215"
        })
        assert response.status_code == 400
        assert response.json.get('error')

    def test_address1_required_field(self, client):
        response = client.post("/profile", data={
            "name": "admin",
            "address1": "",
            "address2": "3646 Bates Brothers Road",
            "city": "Columbus",
            "state": "Ohio",
            "zipcode": "43215"
        })
        assert response.status_code == 400
        assert response.json.get('error')

    def test_city_required_field(self, client):
        response = client.post("/profile", data={
            "name": "admin",
            "address1": "3646 Bates Brothers Road",
            "address2": "3646 Bates Brothers Road",
            "city": "",
            "state": "Ohio",
            "zipcode": "43215"
        })
        assert response.status_code == 400
        assert response.json.get('error')

    def test_zipcode_length(self, client):
        response = client.post("/profile", data={
            "name": "admin",
            "address1": "3646 Bates Brothers Road",
            "address2": "",
            "city": "Columbus",
            "state": "Ohio",
            "zipcode": "5"
        })
        assert response.status_code == 400
        assert response.json.get('error')


class TestFuelQuote:

    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_index(self, client):
        resp = client.get('/fuel-quote')
        assert resp.status_code == 200

    def test_gallons_empty_field(self, client):
        response = client.post("/fuel-quote", data={
            "gallons": ""
        })
        assert response.status_code == 400
        assert response.json.get('error')

    def test_gallons_zero_form(self, client):
        response = client.post("/fuel-quote", data={
            "gallons": "0"
        })
        assert response.status_code == 400
        assert response.json.get('error')

    def test_delivery_date_empty(self, client):
        response = client.post("/fuel-quote", data={
            "gallons": "5",
            "delivery_date": None
        })
        assert response.status_code == 400
        assert response.json.get('error')

    def test_both_empty_form(self, client):
        response = client.post("/fuel-quote", data={
            "gallons": "",
            "delivery_date": None
        })
        assert response.status_code == 400
        assert response.json.get('error')

    def test_both_valid_form(self, client):
        response = client.post("/fuel-quote", data={
            "gallons": "5",
            "delivery_date": "2055-03-15"
        })
        assert response.status_code == 200
        assert response.json.get('success')


class TestFuelQuoteHistory:

    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_get_fuel_quote_history(self, client):
        resp = client.get('/history')
        assert resp.status_code == 200
