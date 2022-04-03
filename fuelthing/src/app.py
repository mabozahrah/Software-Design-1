from flask import Flask, render_template, request, jsonify, redirect, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#worked on db all tgt
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'my-secret-key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return UserCredentials.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)
#mariam's work

class UserCredentials(UserMixin, db.Model):
    __tablename__ = "user_credentials"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    password_hashed = db.Column(db.String(250), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    profile = db.relationship("ClientInformation", uselist=False, backref="user")
    fuel_quotes = db.relationship("FuelQuote", back_populates="user")

    def __init__(self, username: str, password_plaintext: str):
        
        self.username = username
        self.password_hashed = self._generate_password_hash(password_plaintext)

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.password_hashed, password_plaintext)

    def set_password(self, password_plaintext: str):
        self.password_hashed = self._generate_password_hash(password_plaintext)

    @staticmethod
    def _generate_password_hash(password_plaintext):
        return generate_password_hash(password_plaintext)

    def __repr__(self):
        return f'<UserCredentials: {self.username}>'

    @property
    def is_authenticated(self):
        
        return True

    @property
    def is_active(self):
        
        return True

    @property
    def is_anonymous(self):
        
        return False

    def get_id(self):
        
        return str(self.id)


class ClientInformation(db.Model):
    __tablename__ = "client_information"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255), unique=False)
    address1 = db.Column(db.String(255), unique=False)
    address2 = db.Column(db.String(255), unique=False)
    city = db.Column(db.String(255), unique=False)
    state = db.Column(db.String(255), unique=False)
    zipcode = db.Column(db.String(255), unique=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_credentials.id'))

    def __repr__(self):
        return '<ClientInformation %r>' % self.full_name

#brooke's work
class FuelQuote(db.Model):
    __tablename__ = "fuel_quote"
    id = db.Column(db.Integer, primary_key=True)
    gallons = db.Column(db.Integer, unique=False)
    delivery_date = db.Column(db.String(250), nullable=False)
    delivery_address = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_credentials.id"))
    user = db.relationship("UserCredentials", back_populates="fuel_quotes")


@app.before_first_request
def create_table():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Already registered!',category='info')
        return redirect(url_for('quote_history'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            if UserCredentials.query.filter_by(username=username).first():

                return redirect(url_for('login'))
            else:
                new_user = UserCredentials(username, password)
                db.session.add(new_user)
                db.session.commit()
                flash('Thanks for registering, {}!'.format(new_user.username), category='info')
                return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Already logged in!',category='info')
        return redirect(url_for('quote_history'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            user = UserCredentials.query.filter_by(username=username).first()
            if user is not None:
                if user.is_password_correct(password):
                    login_user(user)

                    flash('Thanks for logging in, {}!'.format(current_user.username),category='info')
                    return redirect('/')
                else:
                    return render_template('login.html')
        else:
            return render_template('login.html')
    return render_template('login.html')

#mariam and may

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_profile = ClientInformation.query.get(current_user.id)
    if request.method == 'POST':
        name = request.form.get("name")
        address1 = request.form.get("address1")
        address2 = request.form.get("address2")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")
        print(name, address1, address2, city, state, zipcode)
        if name == '':
            return render_template('profile.html', profile=user_profile)
        if len(name) > 100:
            return render_template('profile.html', profile=user_profile)

        if address1 == '':
            return render_template('profile.html', profile=user_profile)
        if len(address1) > 100 or len(address1) <= 0:
            return render_template('profile.html', profile=user_profile)

        if len(city) > 100 or len(city) <= 0:
            return render_template('profile.html', profile=user_profile)

        if state == "":
            return render_template('profile.html', profile=user_profile)

        if len(zipcode) > 8 or len(zipcode) < 5:
            return render_template('profile.html', profile=user_profile)

        if user_profile:
            user_profile.full_name = name
            user_profile.address1 = address1
            user_profile.address2 = address2
            user_profile.city = city
            user_profile.state = state
            user_profile.zipcode = zipcode
            db.session.commit()
        else:
            user_profile = ClientInformation(full_name=name, address1=address1, address2=address2,
                                         city=city, state=state, zipcode=zipcode, user_id=current_user.id)
            db.session.add(user_profile)
            db.session.commit()
        print(name, address1, address2, city, state, zipcode)
        return redirect(url_for('quote_history'))
    return render_template('profile.html', profile=user_profile)

#brooke and may
@app.route('/fuel-quote', methods=['GET', 'POST'])
@login_required
def fuel_quote():
    if request.method == 'POST':
        gallons = request.form.get('gallons')
        delivery_date = request.form.get('delivery_date')
        delivery_address = request.form.get('delivery_address')
        price = request.form.get('price')
        print(gallons, delivery_date)
        if gallons == '':
            return render_template('quote.html')
        if gallons == '' and delivery_date is None:
            return render_template('quote.html')
        if int(gallons) <= 0:
            return render_template('quote.html')
        if not delivery_address:
            return render_template('quote.html')
        if not delivery_date:
            return render_template('quote.html')
        print(gallons, delivery_date)
        quote = FuelQuote(gallons=gallons, delivery_date=delivery_date,  user=current_user,
                          price=price, delivery_address=delivery_address)
        db.session.add(quote)
        db.session.commit()
        return redirect(url_for('quote_history'))

    return render_template('quote.html')


@app.route('/')
@login_required
def quote_history():
    fuel_quotes = FuelQuote.query.filter_by(user=current_user).all()
    print(fuel_quotes)
    return render_template('quote-history.html', fuel_quotes=fuel_quotes)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Goodbye!',category='info')
    return redirect(url_for('login'))

#may's work
class Pricing:
    def __init__(self, gallons, delivery_address, delivery_date):
        self.gallons = gallons
        self.delivery_address = delivery_address
        self.delivery_date = delivery_date


if __name__ == '__main__':
    app.run(debug=True)
