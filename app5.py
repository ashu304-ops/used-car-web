import os
import json
import uuid
from flask import Flask, render_template, request, redirect, url_for, make_response, flash, jsonify
from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm, UploadForm, ContactForm

app = Flask(__name__)
# Load secret key from an environment variable in production
app.config['SECRET_KEY'] = 'your_very_secure_secret_key_here'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Local database files
CARS_DATA_FILE = 'cars.json'
USERS_DATA_FILE = 'users.json'
CONTACTS_DATA_FILE = 'contacts.json'

class User(UserMixin):
    def __init__(self, id):
        self.id = id
    
    @staticmethod
    def get(user_id):
        if not os.path.exists(USERS_DATA_FILE):
            return None
        with open(USERS_DATA_FILE, 'r') as f:
            users_data = json.load(f)
            if user_id in users_data:
                return User(user_id)
            return None

def load_cars():
    if not os.path.exists(CARS_DATA_FILE):
        return []
    with open(CARS_DATA_FILE, 'r') as f:
        return json.load(f)

def save_cars(cars):
    with open(CARS_DATA_FILE, 'w') as f:
        json.dump(cars, f, indent=4)

def save_contact_message(message):
    if not os.path.exists(CONTACTS_DATA_FILE):
        with open(CONTACTS_DATA_FILE, 'w') as f:
            json.dump([], f)
    
    with open(CONTACTS_DATA_FILE, 'r+') as f:
        contacts = json.load(f)
        contacts.append(message)
        f.seek(0)
        json.dump(contacts, f, indent=4)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    if os.path.exists(USERS_DATA_FILE):
        return User.get(user_id)
    return None

@app.route('/')
def index():
    cars = load_cars()
    response = make_response(render_template('index.html', cars=cars))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/services', methods=['GET', 'POST'])
def services():
    form = ContactForm()
    if form.validate_on_submit():
        contact_data = {
            'name': form.name.data,
            'email': form.email.data,
            'message': form.message.data
        }
        save_contact_message(contact_data)
        return jsonify(success=True, message='Message sent successfully!')
    return render_template('services.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not os.path.exists(USERS_DATA_FILE):
            with open(USERS_DATA_FILE, 'w') as f:
                json.dump({}, f)
        
        with open(USERS_DATA_FILE, 'r') as f:
            users_data = json.load(f)
        
        if form.username.data in users_data:
            flash('Username already exists.', 'danger')
            return jsonify(success=False, message='Username already exists.')
        
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        users_data[form.username.data] = {'password': hashed_password}
        
        with open(USERS_DATA_FILE, 'w') as f:
            json.dump(users_data, f, indent=4)
        
        flash('Registration successful! Please log in.', 'success')
        return jsonify(success=True)
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if not os.path.exists(USERS_DATA_FILE):
            return jsonify(success=False, message='Invalid username or password.')
        
        with open(USERS_DATA_FILE, 'r') as f:
            users_data = json.load(f)

        user_id = form.username.data
        password = form.password.data

        if user_id in users_data and bcrypt.check_password_hash(users_data[user_id]['password'], password):
            user = User(user_id)
            login_user(user)
            return jsonify(success=True, redirect_url=url_for('upload'))
        else:
            return jsonify(success=False, message='Invalid username or password.')

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            errors = form.errors
            return jsonify(success=False, message=str(errors))

        make = form.make.data
        model = form.model.data
        year = form.year.data
        price = form.price.data
        details = form.details.data
        
        photos = request.files.getlist('photos')
        
        photo_filenames = []
        if photos and photos[0].filename != '':
            for file in photos:
                if file and allowed_file(file.filename):
                    filename_uuid = str(uuid.uuid4())
                    ext = file.filename.rsplit('.', 1)[1].lower()
                    filename = secure_filename(f'{filename_uuid}.{ext}')
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    photo_filenames.append(filename)

        new_car = {
            'id': str(uuid.uuid4()),
            'make': make,
            'model': model,
            'year': year,
            'price': price,
            'details': details,
            'photos': photo_filenames
        }
        
        cars = load_cars()
        cars.append(new_car)
        save_cars(cars)

        return jsonify(success=True, message='Car uploaded successfully!')

    return render_template('upload.html', form=form)

@app.route('/delete_car/<string:car_id>', methods=['POST'])
@login_required
@csrf.exempt
def delete_car(car_id):
    cars = load_cars()
    car_to_delete = None
    for car in cars:
        if car['id'] == car_id:
            car_to_delete = car
            break

    if car_to_delete:
        # Delete image files
        for photo_filename in car_to_delete['photos']:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Remove car from list
        cars.remove(car_to_delete)
        save_cars(cars)
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create necessary directories and files if they don't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(CARS_DATA_FILE):
        with open(CARS_DATA_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(USERS_DATA_FILE):
        with open(USERS_DATA_FILE, 'w') as f:
            json.dump({}, f)
    if not os.path.exists(CONTACTS_DATA_FILE):
        with open(CONTACTS_DATA_FILE, 'w') as f:
            json.dump([], f)
    
    app.run(debug=True)
