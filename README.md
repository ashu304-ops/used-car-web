Aash Auto Works Pvt Ltd
Project Overview
This project is a Flask-based web application for Aash Auto Works Pvt Ltd, a certified used car seller. The website features a public-facing section for users to view car listings and a secure client-only section for clients to manage car inventory.

Features
Professional, Dark-Themed UI: A sleek, modern user interface.

Public Car Listings: Users can view all available cars with interactive photo carousels.

Client-Side Uploads: Clients can securely log in to upload new car listings, including details and multiple photos.

Live Preview and Cropping: The upload page includes an image cropping tool and a live preview of the listing before submission.

Secure Authentication: User registration and login are protected using Flask-Bcrypt for password hashing and Flask-Login for session management.

CSRF Protection: All forms are protected against Cross-Site Request Forgery (CSRF) attacks using Flask-WTF.

Local Data Storage: All car listings and user accounts are stored in local cars.json and users.json files, making the application completely free for testing and development.

Setup and Installation
Prerequisites
Make sure you have Python installed on your system.

Install Dependencies
Open your terminal or command prompt and run the following command to install all the required Python libraries:

pip install Flask Flask-Bcrypt Flask-Login Flask-WTF Werkzeug

File Structure
Ensure your project directory is set up with the following structure:

used_car_website/
├── app.py
├── forms.py
├── cars.json
├── users.json
├── templates/
│   ├── index.html
│   ├── services.html
│   ├── login.html
│   ├── register.html
│   └── upload.html
└── static/
    ├── css/
    │   └── style.css
    └── uploads/

Note: The cars.json and users.json files will be created automatically when you run the application for the first time.

Running the Application
Navigate to your project directory in the terminal.

Run the application with the following command:

python app.py

Open your web browser and navigate to http://127.0.0.1:5000/.

Client Login
The client login is not publicly linked for security reasons. To access the client-side features, navigate directly to the login page:
http://127.0.0.1:5000/login

You will need to register a new client account from the login page before you can upload car listings.
