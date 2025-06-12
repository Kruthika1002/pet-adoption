# 🐾 Pet Adoption Management System

A full-stack Pet Adoption Management System with admin authentication, graphical pet management, and real-time MySQL database integration.

# Screenshots

## login page
 ![Login Page](static/images/login page.png)

## 👩‍💻 Contributors
- Developed by: Kruthika S and team
- Technologies: Python (Tkinter, Flask), MySQL, HTML/CSS/JS

---

## 🚀 Features

- 🔐 **Login System**: Admin authentication using Flask with session management.
- 🐶 **Pet Dashboard**: Add, update, delete, and view pets with images using a Tkinter GUI.
- 📅 **Rescue Details**: Record pet age, rescue date, category, and adoption status.
- 📊 **Report Generation**: Generate pet statistics by category and adoption status.
- 🛠️ **Persistent Storage**: Data stored in a MySQL database (`petadoption`).
- 🌐 **Responsive Login UI**: Styled login page using HTML, CSS, and JavaScript.

---

## 🧾 File Structure

```bash
project/
├── main.py               # Tkinter GUI for pet management
├── database.py           # Database connection and CRUD functions
├── login_handler.py      # Flask routes and session-based login
├── login.js              # Frontend script for login page interaction
├── style.css             # Responsive login page styling
├── petadoption.sql       # SQL schema and initial data for MySQL
└── README.md             # Project documentation
```

---

## 🗃️ Database Setup

1. Create the database:
```sql
CREATE DATABASE petadoption;
USE petadoption;
```

2. Run `petadoption.sql` to create tables and insert initial admin credentials.

3. Default login credentials:
```
Username: admin
Password: admin123
```

---

## 💻 How to Run

### 🔹 Backend + GUI

```bash
# Install dependencies
pip install flask mysql-connector-python pillow tkcalendar

# Start Flask app
python login_handler.py

# The GUI will launch upon successful login at /login
```


## 🛡️ Security Note

- 🔑 Change `app.secret_key` in `login_handler.py` to a secure value.
- 🔒 Store passwords securely using hashing (e.g., bcrypt) instead of plain text.


## 📈 Future Enhancements

- ✅ User role management (Admin/Staff)
- 📷 Cloud storage for pet images
- 🌐 Full web-based dashboard
- 📱 Mobile-friendly frontend


## 📜 License

This project is for academic purposes under RV University guidelines.
