from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

user_info = {
    'username': 'admin',
    'password': 'secret-password'
}

#Mariam
@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('signup.html')

#Mariam
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username, password)
        if username == user_info['username'] and password == user_info['password']:
            print('login successful')
            print(username, password)
            return jsonify({'success': 'login successful'}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 400
    return render_template('login.html'), 200

#Mariam
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        name = request.form.get("name")
        address1 = request.form.get("address1")
        address2 = request.form.get("address2")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")
        print(name, address1, address2, city, state, zipcode)
        if name == '':
            return jsonify({"error": "A name is required"}), 400
        if len(name) > 100:
            return jsonify({"error": "Name can only be up to 150 characters."}), 400

        if address1 == '':
            return jsonify({"error": "Address is required"}), 400
        if len(address1) > 100 or len(address1) <= 0:
            return jsonify({"error": "Address 1 can only be up to 100 characters"}), 400

        if len(address2) > 100:
            return jsonify({"error": "Address 2 can only be up to 100 characters"}), 400

        if len(city) > 100 or len(city) <= 0:
            return jsonify({"error": "city is required & can only be up to 100 characters"}), 400

        if state == "":
            return jsonify({"error": "state is required"}), 400

        if len(zipcode) > 8 or len(zipcode) < 5:
            return jsonify({"error": "zipcode is required & must be between 5-8 characters"}), 400

        print(name, address1, address2, city, state, zipcode)
        return jsonify({"success": "Profile Updated"}), 200
    return render_template('profile.html'), 200

#Brooke and May
@app.route('/fuel-quote', methods=['GET', 'POST'])
def fuel_quote():
    if request.method == 'POST':
        gallons = request.form.get('gallons')
        delivery_date = request.form.get('delivery_date')

        print(gallons, delivery_date)
        if gallons == '':
            return jsonify({"error": "Gallons is required"}), 400
        if gallons == '' and delivery_date is None:
            return jsonify({"error": "Both field is required"}), 400
        if int(gallons) <= 0:
            return jsonify({"error": "Gallons must be greater than 0"}), 400

        if not delivery_date:
            return jsonify({"error": "Delivery date is required"}), 400
        print(gallons, delivery_date)
        return jsonify({"success": "Fuel Quote Submitted"}), 200
    return render_template('quote.html'), 200

#Brooke and May
@app.route('/history')
def quote_history():
    return render_template('quote-history.html'), 200


class Pricing:
    def __init__(self, gallons, delivery_address, delivery_date):
        self.gallons = gallons
        self.delivery_address = delivery_address
        self.delivery_date = delivery_date


if __name__ == '__main__':
    app.run()
