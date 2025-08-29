

````markdown
# 🚗 Aash Auto Works Pvt Ltd - Used Car Dealer Web App

A Flask-based web application built for **Aash Auto Works Pvt Ltd**, a certified used car seller.  
The website features a **public-facing section** for users to view car listings and a **secure client-only section** for uploading and managing inventory.

---

## 🔧 Features

- **🌙 Professional, Dark-Themed UI** – Sleek and modern design
- **🖼️ Public Car Listings** – View all available cars with interactive photo carousels
- **🔐 Secure Client Login** – Only verified clients can access upload features
- **📤 Client-Side Uploads** – Add car details and multiple images with a simple form
- **🖼️ Live Image Cropping** – Crop and preview images before uploading
- **🔒 Secure Authentication** – Passwords hashed with Flask-Bcrypt and session management via Flask-Login
- **🛡️ CSRF Protection** – All forms protected using Flask-WTF
- **💾 Local Storage** – All data stored in local `.json` files (no database needed)

---

## 🚀 Setup and Installation

### ✅ Prerequisites
- Python 3.x installed on your system

### 📦 Install Dependencies

Run this in your terminal:

```bash
pip install Flask Flask-Bcrypt Flask-Login Flask-WTF Werkzeug
````

---

## 📁 File Structure

```
used_car_website/
├── app.py
├── forms.py
├── cars.json          # Auto-created
├── users.json         # Auto-created
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
```

📝 Note: `cars.json` and `users.json` are created automatically when you first run the app.

---

## ▶️ Running the Application

1. Navigate to the project directory:

```bash
cd used_car_website
```

2. Start the Flask server:

```bash
python app.py
```

3. Open your browser and go to:

```
http://127.0.0.1:5000/
```

---

## 🔐 Client Access

The client login page is not publicly linked for security.

To access the client dashboard:

```
http://127.0.0.1:5000/login
```

From there, you can **register a new client account** to log in and start uploading car listings.

---

## 📸 Upload Features

* Upload multiple car images
* Live image preview and cropping
* Auto-generated JSON-based database for listing storage

---

## 💡 Notes

* This project uses local `.json` files for user and car data, ideal for development and testing.
* For production deployment, consider migrating to a proper database (like PostgreSQL or MongoDB).

---

## 📃 License

This project is for educational and demo purposes only. Contact the project owner for commercial 
```
## Author
 Ashish Sureshbabu
