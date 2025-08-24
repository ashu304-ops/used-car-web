import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# In-memory list to store car data (for demonstration purposes)
cars = []

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Route for the user-facing car listings page."""
    return render_template('index.html', cars=cars)

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
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                photo_filenames.append(file_path)

        new_car = {
            'id': len(cars) + 1,
            'make': make,
            'model': model,
            'year': year,
            'price': price,
            'details': details,
            'photos': photo_filenames
        }
        cars.append(new_car)

        return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    # Create the upload folder if it doesn't exist on startup
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
