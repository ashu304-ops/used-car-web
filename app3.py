import os
import json
import uuid
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response, flash
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_very_secure_secret_key_here'  # Change this to a random, secure key
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Local database files
CARS_DATA_FILE = 'cars.json'
USERS_DATA_FILE = 'users.json'

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @staticmethod
    def get(user_id):
        users = load_users()
        return User(user_id) if user_id in users else None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data(file_path, default_value):
    """Loads data from a JSON file."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default_value
    return default_value

def save_data(file_path, data):
    """Saves data to a JSON file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def load_cars():
    return load_data(CARS_DATA_FILE, [])

def save_cars(cars_list):
    save_data(CARS_DATA_FILE, cars_list)

def load_users():
    return load_data(USERS_DATA_FILE, {})

def save_users(users_dict):
    save_data(USERS_DATA_FILE, users_dict)

@app.route('/')
def index():
    cars = load_cars()
    response = make_response(render_template('index.html', cars=cars))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in users:
            flash("User already exists. Please choose a different username.")
            return redirect(url_for('register'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users[username] = {'password': hashed_password}
        save_users(users)
        flash("Registration successful! You can now log in.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        
        if username in users and bcrypt.check_password_hash(users[username]['password'], password):
            user = User(username)
            login_user(user)
            return redirect(url_for('upload'))
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        details = request.form['details']

        uploaded_files = request.files.getlist('photos')
        photo_filenames = []
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}-{filename}"
                
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                photo_filenames.append(os.path.join('static', 'uploads', unique_filename))

        cars = load_cars()
        new_car = {
            'id': len(cars) + 1,
            'make': make,
            'model': model,
            'year': int(year),
            'price': price,
            'details': details,
            'photos': photo_filenames
        }
        cars.append(new_car)
        save_cars(cars)
        return redirect(url_for('index'))
    return render_template('upload.html')

@app.route('/delete_car/<car_id>', methods=['POST'])
@login_required
def delete_car(car_id):
    cars = load_cars()
    cars_to_keep = [car for car in cars if str(car['id']) != car_id]
    save_cars(cars_to_keep)
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(CARS_DATA_FILE):
        save_cars([])
    if not os.path.exists(USERS_DATA_FILE):
        save_users({})
    app.run(debug=True)
