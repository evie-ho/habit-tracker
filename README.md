# 🚀 Habit Tracker Web Application

A full-featured Flask web application for tracking daily habits, building streaks, and monitoring personal progress. Perfect for building consistent routines and achieving personal goals.

## 🚀 Live Demo
https://habit-tracker-evieho.onrender.com

## 🎯 Features
- **User Authentication** - Secure registration and login system
- **Habit Management** - Full CRUD operations (Create, Read, Update, Delete)
- **Streak Tracking** - Visual streak counter for motivation
- **Completion History** - View detailed history for each habit
- **User Profiles** - Personal statistics and progress tracking
- **Responsive Design** - Works on desktop and mobile devices
- **Flash Messages** - User-friendly feedback system

## 🛠️ Technologies Used
- **Backend**: Python, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Password hashing with Werkzeug
- **Styling**: Custom CSS with modern gradient design

## 📋 Prerequisites
- Python 3.8+
- pip (Python package manager)

## 🚀 Installation & Setup

### Local Development
1. **Clone the repository**
   ```bash
   git clone https://github.com/themrsfitho/habit-tracker.git
   cd habit-tracker
<<<<<<< HEAD
Create and activate virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Run the application

bash
python app.py
Open your browser
Navigate to http://localhost:5000

Quick Start with Docker (Optional)
bash
# Build and run with Docker
docker build -t habit-tracker .
docker run -p 5000:5000 habit-tracker
📁 Project Structure

text
habit-tracker/
├── app.py                 # Main Flask application
├── models.py              # Database models (User, Habit, HabitLog)
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore file
├── static/
│   └── style.css         # Custom CSS styles
├── templates/            # HTML templates
│   ├── index.html        # Home/Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── habits.html       # Habits dashboard
│   ├── add_habit.html    # Add new habit form
│   ├── history.html      # Habit completion history
│   └── profile.html      # User profile page
├── instance/             # Database instance
│   └── habit_tracker.db  # SQLite database (auto-generated)
└── screenshots/          # Application screenshots


🔧 API Endpoints
Method	Route	Description	Authentication Required
GET	/	Home page	No
GET, POST	/register	User registration	No
GET, POST	/login	User login	No
GET	/logout	User logout	Yes
GET	/habits	View all habits	Yes
GET, POST	/add_habit	Add new habit	Yes
POST	/complete_habit/<id>	Mark habit as complete	Yes
POST	/delete_habit/<id>	Delete a habit	Yes
GET	/history/<id>	View habit history	Yes
GET	/profile	User profile	Yes



🗄️ Database Schema
sql
-- Users table
CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Habits table  
CREATE TABLE habit (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    frequency TEXT DEFAULT 'daily',
    created_date DATE NOT NULL,
    user_id INTEGER REFERENCES user(id)
);

-- Habit logs table
CREATE TABLE habit_log (
    id INTEGER PRIMARY KEY,
    habit_id INTEGER REFERENCES habit(id),
    completed_date DATE NOT NULL,
    notes TEXT
);


🧪 Testing
Run basic tests:

bash
python -m pytest tests/ -v
