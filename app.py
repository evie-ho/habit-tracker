"""
Habit Tracker Flask Application
Main application file with all routes and logic
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import date
from models import db, User, Habit, HabitLog

# Initialize Flask app first
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'dev-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habit_tracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
db.init_app(app)

# ======================
# HELPER FUNCTIONS
# ======================
def get_current_user():
    """Get current logged in user"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

def calculate_streak(habit):
    """Calculate current streak for a habit"""
    if not habit.logs:
        return 0
    
    # Get dates when habit was completed, sorted most recent first
    completed_dates = sorted([log.completed_date for log in habit.logs], reverse=True)
    
    streak = 0
    current_date = date.today()
    
    # Check if habit was completed today or yesterday to start streak
    if completed_dates and (completed_dates[0] == current_date or 
                           completed_dates[0] == current_date.replace(day=current_date.day-1)):
        streak = 1
        for i in range(1, len(completed_dates)):
            if (completed_dates[i-1] - completed_dates[i]).days == 1:
                streak += 1
            else:
                break
    return streak

# ======================
# ROUTES
# ======================

@app.route('/')
def index():
    """Home page - redirects to habits if logged in, otherwise to login"""
    if 'user_id' in session:
        return redirect(url_for('view_habits'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if user exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(username=username)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('view_habits'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/habits')
def view_habits():
    """View all habits for current user"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    habits = Habit.query.filter_by(user_id=user.id).all()
    
    # Calculate streaks for each habit
    habits_with_streaks = []
    for habit in habits:
        streak = calculate_streak(habit)
        habits_with_streaks.append({
            'habit': habit,
            'streak': streak
        })
    
    return render_template('habits.html', habits=habits_with_streaks, user=user)

@app.route('/add_habit', methods=['GET', 'POST'])
def add_habit():
    """Add a new habit"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form.get('description', '')
        frequency = request.form.get('frequency', 'daily')
        
        new_habit = Habit(
            name=name,
            description=description,
            frequency=frequency,
            user_id=user.id,
            created_date=date.today()
        )
        
        db.session.add(new_habit)
        db.session.commit()
        
        flash('Habit added successfully!')
        return redirect(url_for('view_habits'))
    
    return render_template('add_habit.html')

@app.route('/complete_habit/<int:habit_id>', methods=['POST'])
def complete_habit(habit_id):
    """Mark a habit as completed for today"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    habit = Habit.query.get_or_404(habit_id)
    
    # Check if user owns this habit
    if habit.user_id != user.id:
        flash('You do not have permission to complete this habit')
        return redirect(url_for('view_habits'))
    
    # Check if already completed today
    today = date.today()
    existing_log = HabitLog.query.filter_by(
        habit_id=habit_id,
        completed_date=today
    ).first()
    
    if existing_log:
        flash('Habit already completed today!')
    else:
        # Create new log entry
        new_log = HabitLog(
            habit_id=habit_id,
            completed_date=today,
            notes=request.form.get('notes', '')
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Habit marked as complete! Great job!')
    
    return redirect(url_for('view_habits'))

@app.route('/delete_habit/<int:habit_id>', methods=['POST'])
def delete_habit(habit_id):
    """Delete a habit"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    habit = Habit.query.get_or_404(habit_id)
    
    # Check if user owns this habit
    if habit.user_id != user.id:
        flash('You do not have permission to delete this habit')
        return redirect(url_for('view_habits'))
    
    # Delete associated logs first
    HabitLog.query.filter_by(habit_id=habit_id).delete()
    
    # Delete the habit
    db.session.delete(habit)
    db.session.commit()
    
    flash('Habit deleted successfully!')
    return redirect(url_for('view_habits'))

@app.route('/history/<int:habit_id>')
def view_history(habit_id):
    """View completion history for a habit"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    habit = Habit.query.get_or_404(habit_id)
    
    # Check if user owns this habit
    if habit.user_id != user.id:
        flash('You do not have permission to view this habit')
        return redirect(url_for('view_habits'))
    
    logs = HabitLog.query.filter_by(habit_id=habit_id).order_by(HabitLog.completed_date.desc()).all()
    streak = calculate_streak(habit)
    
    return render_template('history.html', habit=habit, logs=logs, streak=streak)

@app.route('/profile')
def profile():
    """User profile page"""
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    
    total_habits = Habit.query.filter_by(user_id=user.id).count()
    
    # Get completion stats
    today = date.today()
    habits_completed_today = 0
    
    for habit in user.habits:
        if HabitLog.query.filter_by(habit_id=habit.id, completed_date=today).first():
            habits_completed_today += 1
    
    return render_template('profile.html', 
                         user=user, 
                         total_habits=total_habits,
                         habits_completed_today=habits_completed_today)
    total_habits = Habit.query.filter_by(user_id=user.id).count()
    
    # Get completion stats
    today = date.today()
    habits_completed_today = 0
    for habit in user.habits:
        if HabitLog.query.filter_by(habit_id=habit.id, completed_date=today).first():
            habits_completed_today += 1
    
    return render_template('profile.html', 
                         user=user, 
                         total_habits=total_habits,
                         habits_completed_today=habits_completed_today)

# ======================
# INITIALIZATION
# ======================

def init_database():
    """Initialize database tables"""
    with app.app_context():
        db.create_all()
        print("✓ Database tables created/verified")

if __name__ == '__main__':
    # Initialize database before first request
    init_database()
    app.run(debug=True)