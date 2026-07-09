# Task Management System (TMS)

A professional, responsive administrative web portal built using Python, Flask, and MySQL. This system allows administrators to log in securely, view employee tasks, and dynamically update completion states.

Designed with a focus on code readability, separation of concerns, and clean visual aesthetics, this project is ideal for student assignment submissions and local demonstrations.

---

## 📖 Table of Contents
1. [Project Description](#-project-description)
2. [Features](#-features)
3. [Technology Stack](#-technology-stack)
4. [Folder Structure](#-folder-structure)
5. [Installation & Setup](#-installation--setup)
6. [Environment Variables](#-environment-variables)
7. [Running the Project](#-running-the-project)
8. [API Endpoints](#-api-endpoints)
9. [Screenshots](#-screenshots)
10. [Future Improvements](#-future-improvements)
11. [License](#-license)

---

## 🌟 Project Description

The **Task Management System** provides a clean web-based interface for operations managers or supervisors to monitor tasks assigned to employees. The application features a secure login system for administrative staff, an interactive dashboard that loads task-specific employee metadata in real-time, and database persistence to save the status updates.

This implementation has been refactored to prioritize clean programming principles, separating query execution logic into a dedicated database module and using configuration files to prevent hardcoded credentials.

---

## ⚡ Features

- **Secure Authentication:** Admin-only login with session handling and flash message alerts.
- **Dynamic Dashboard UI:** Select tasks from a dropdown menu to immediately display the corresponding Employee ID and Name without reloading the page.
- **Robust Database Helper Module:** Automatic schema checking, database creation, and sample data seeding on startup.
- **Configurable Environment:** Separation of credentials from source code using environment variables (`.env`).
- **Premium Responsive Styling:** Crafted using modern CSS (variables, glassmorphic panels, and backdrop blurs) for a clean look on both desktop and mobile viewports.

---

## 🛠️ Technology Stack

- **Backend:** Python (Flask web framework)
- **Database:** MySQL
- **Frontend:** HTML5, Custom Vanilla CSS3, Modern ES6 Javascript
- **Environment Configuration:** python-dotenv

---

## 📁 Folder Structure

```text
task-management-system/
│
├── static/
│   ├── css/
│   │   └── style.css          # Premium, modern responsive styles
│   └── js/
│       └── main.js            # Interactivity and DOM updates
│
├── templates/
│   ├── login.html             # Secure login screen template
│   └── dashboard.html         # Panel dashboard template
│
├── .env.example               # Template file for environment variables
├── .gitignore                 # Files excluded from git version control
├── app.py                     # Main application entry point & routing
├── database.py                # Database connection, schemas, and queries
├── requirements.txt           # Declared python dependencies
└── README.md                  # Project documentation
```

---

## ⚙️ Installation & Setup

Follow these steps to configure the project on your local machine:

### Prerequisite
Ensure you have the following installed:
- Python 3.8 or higher
- MySQL Server (e.g., MySQL Community Server or via XAMPP/WampServer)

### 1. Clone/Setup Workspace
Extract or navigate into the root directory of the project:
```bash
cd Task-Management-System
```

### 2. Set Up Virtual Environment (Recommended)
Create and activate a python virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install all package requirements using `pip`:
```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

The project utilizes environment variables for database configurations and session security. 

1. Copy the `.env.example` file and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and replace the placeholders with your local MySQL credentials:

```ini
# Flask Secret Session Key
FLASK_SECRET_KEY=your_super_secret_session_key_here

# MySQL Configuration
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=task_manager_db
```

---

## 🚀 Running the Project

### Step 1: Initial Database Setup
Run the `database.py` script once. This creates the database and required tables on your MySQL server, and populates them with default administrative credentials and sample tasks.
```bash
python database.py
```
*Note: If the MySQL server credentials are correct, the database `task_manager_db` will be initialized automatically.*

### Step 2: Start the Web Server
Launch the Flask development server:
```bash
python app.py
```

### Step 3: Access the Application
Open your web browser and navigate to:
```text
http://127.0.0.1:5000/
```

### 🔐 Default Admin Credentials
To bypass the login screen, use the pre-seeded admin login details:
- **Admin ID:** `admin`
- **Password:** `admin123`

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/` | Displays the administrator login panel. Redirects to `/dashboard` if logged in. |
| **POST** | `/` | Validates admin credentials and starts a login session. |
| **GET** | `/dashboard` | Displays the task control panel (requires authentication). |
| **POST** | `/dashboard` | Processes task completion state updates. |
| **GET** | `/logout` | Revokes the current session and redirects to the login panel. |

---

## 📸 Screenshots

Here are placeholders for application visual demonstrations:

#### 1. Administrative Login Portal
> *[Placeholder: Add your login portal screenshot here]*

#### 2. Task Management Dashboard Panel
> *[Placeholder: Add your dashboard screenshot here]*

---

## 🔮 Future Improvements

If you wish to extend the scope of this project, consider adding:
1. **Interactive CRUD Operations:** Allow administrators to add new tasks, edit assignee names, or delete tasks directly through the UI.
2. **Password Hashing:** Hash administrator passwords (e.g., using `bcrypt` or `werkzeug.security`) before storing them.
3. **Advanced Analytics:** Incorporate a visual progress ring or bar chart (using `Chart.js`) showing the percentage of completed tasks.
4. **Role-Based Access Control:** Allow standard employees to sign in and view their specific tasks, while restricting status changes to administrative accounts.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
