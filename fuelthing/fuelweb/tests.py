import unittest
from django.test import TestCase, Client

# Create your tests here.

class indexTests(TestCase):
    def set_up(self):
        self.client = Client()

    """ test homepage returns 200 status """
    def test_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class LoginTests(TestCase):
    def set_up(self):
        self.client = Client()

    """ test login page returns 200 status for GET """
    def test_status(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    """ Testing submission of a login that fits the form requirements """
    def test_good_login(self):
        response = self.client.post(
            "/login", data={'username': 'shortusername', 'password': 'shortpassword'}
        ) 
        # verify that response is a redirect (successful POST)
        self.assertEqual(response.status_code, 200)

    """ Testing submission of a login that does not fit the form requirements """
    def test_bad_login(self):
        response = self.client.post(
            "/login", data={'username': 'definitelyovertwentycharactermaximum',
            'password': 'randompassword'}
        ) 
        # verify that response is NOT a redirect (i.e. it submits another GET request)
        self.assertEqual(response.status_code, 200)

class RegistrationTests(TestCase):
    def set_up(self):
        self.client = Client()

    """ test registration page returns 200 status for GET """
    def test_status(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    """ Testing submission of a registration that fits the form requirements """
    def test_good_registration(self):
        response = self.client.post(
            "/register", data={'username': 'shortusername', 'password': 'shortpassword',
            'confirm_password': 'shortconfirmation'}
        ) 
        # verify that response is a 200 (successful POST)
        self.assertEqual(response.status_code, 200)

    """ Testing submission of a registration that does not fit the form requirements """
    def test_bad_registration(self):
        response = self.client.post(
            "/register", data={'username': 'definitelyovertwentycharactermaximum',
            'password': 'randompassword',
            'confirm_password': 'randompassword'}
        ) 
        # verify that response is NOT a redirect (i.e. it submits another GET request)
        self.assertEqual(response.status_code, 200)

class QuoteFormTests(TestCase):
    def set_up(self):
        self.client = Client()

    """ test quote page returns 200 status for GET """
    def test_status(self):
        response = self.client.get("/quote")
        self.assertEqual(response.status_code, 302)
    
    """ validating a quote form that fits the form requirements """
    def quote_form_is_valid(self):
        response = self.client.post(
            "/quote", data={'gallons': 'zeroormore', 
            'date': 'randomdate'}
        )
        # verify that response is a redirect (successful POST)
        self.assertEqual(response.status_code, 302)

    """ validating a quote form that does not fit the form requirements """
    def quote_form_is_invalid(self):
        response = self.client.post(
            "/quote", data={'gallons': 'lessthan0',
            'date': 'nodate'}
        )
        # verify that response is NOT a redirect (i.e. it submits another GET request)
        self.assertEqual(response.status_code, 200)

class HistoryTests(TestCase):
    def set_up(self):
        self.client = Client()

    """ test history page returns 302 status for GET """
    def test_status(self):
        response = self.client.get('/history')
        self.assertEqual(response.status_code, 302)

class ProfileTests(TestCase):
    def set_up(self):
        self.client = Client()

    """ test profile page returns 302 status for GET """
    def test_status(self):
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 302)

    """ validating a profile form that fits the form requirements """
    def profile_form_is_valid(self):
        response = self.client.post(
            "/profile", data={'full_name': 'first middle last',
            'address_1': '123 address dr.',
            'city': 'my city',
            'state': 'tx',
            'zip_code': 77777}
        )
        # verify that response is a redirect (successful POST)
        self.assertEqual(response.status_code, 302)

    """ validating a profile form that does not fit the form requirements """
    def profile_form_is_invalid(self):
        response = self.client.post(
            "/profile", data={'full_name': 'no full name',
            'address_1': 'no address',
            'city': 'no city',
            'state': 'none',
            'zip_code': 0}
        )
        # verify that response is NOT a redirect (i.e. it submits another GET request)
        self.assertEqual(response.status_code, 200)