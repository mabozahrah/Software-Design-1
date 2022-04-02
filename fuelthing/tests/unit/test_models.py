from src.app import UserCredentials,ClientInformation,FuelQuote

#Mariam
def test_new_user():
    
    user = UserCredentials('patkennedy79', 'password1')
    assert user.username == 'patkennedy79'
    assert user.password_hashed != 'password1'
    assert user.__repr__() == '<UserCredentials: patkennedy79>'
    assert user.is_authenticated
    assert user.is_active
    assert not user.is_anonymous

#May
def test_new_user_with_fixture(new_user):
    
    assert new_user.username == 'patkennedy79'
    assert new_user.password_hashed != 'password1'

#May
def test_setting_password(new_user):
    
    new_user.set_password('MyNewPassword')
    assert new_user.password_hashed != 'MyNewPassword'
    assert new_user.is_password_correct('MyNewPassword')
    assert not new_user.is_password_correct('MyNewPassword2')
    assert not new_user.is_password_correct('password1')

#May
def test_user_id(new_user):
    
    new_user.id = 17
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == '17'



#Mariam
def test_new_profile():
    
    profile = ClientInformation(full_name='John Doe', address1='4529 Marcus Street', city="Birmingham",
                                state="AL", zipcode="352030", user_id=7)
    assert profile.full_name == 'John Doe'
    assert profile.address1 == '4529 Marcus Street'
#Brooke
def test_new_profile_with_fixture(new_profile):
    
    assert new_profile.full_name == 'John Doe'
    assert new_profile.address1 == '4529 Marcus Street'
#Brooke
def test_new_fuel_quote():
    
    fuel_quote = FuelQuote(gallons=7, delivery_date='2022-04-2', delivery_address='4529 Marcus Street', price=3.0,
                           user_id=7)

    assert fuel_quote.gallons == 7
    assert fuel_quote.delivery_date == '2022-04-2'
    assert fuel_quote.delivery_address == '4529 Marcus Street'
#Brooke
def test_new_fuel_with_fixture(new_fuel_quote):
    
    assert new_fuel_quote.gallons == 7
    assert new_fuel_quote.delivery_date == '2022-04-2'
    assert new_fuel_quote.delivery_address == '4529 Marcus Street'