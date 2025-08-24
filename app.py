import os
import json
import uuid
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Local database file
CARS_DATA_FILE = 'cars.json'

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_cars():
    """Load car listings from the JSON file."""
    if os.path.exists(CARS_DATA_FILE):
        with open(CARS_DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_cars(cars_list):
    """Save car listings to the JSON file."""
    with open(CARS_DATA_FILE, 'w') as f:
        json.dump(cars_list, f, indent=4)

@app.route('/')
def index():
    """Route for the user-facing car listings page."""
    cars = load_cars()
    response = make_response(render_template('index.html', cars=cars))
    # Add no-cache headers to prevent browser from caching the page
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/services')
def services():
    """Route for the services page."""
    return render_template('services.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Route for clients to upload car information and photos."""
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
                # Generate a unique filename to prevent caching issues
                filename = secure_filename(file.filename)
                unique_filename = f"{uuid.uuid4()}-{filename}"
                
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(file_path)
                photo_filenames.append(os.path.join('static', 'uploads', unique_filename))

        # Load existing cars, add the new car, and save the list
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
def delete_car(car_id):
    """Route to delete a car listing."""
    cars = load_cars()
    cars_to_keep = [car for car in cars if str(car['id']) != car_id]
    save_cars(cars_to_keep)
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    if not os.path.exists(CARS_DATA_FILE):
        save_cars([])
    app.run(debug=True)
