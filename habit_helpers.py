# habit_helpers.py
from app import db, User, Habit
from datetime import date, timedelta
import json

def add_user(username, email):
    if User.query.filter_by(username=username).first():
        print(f"User '{username}' already exists.")
        return None
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    print(f"User '{username}' added.")
    return user

def add_habit(user_id, habit_name):
    habit = Habit.query.filter_by(name=habit_name, user_id=user_id).first()
    if habit:
        print(f"Habit '{habit_name}' already exists for user {user_id}.")
        return habit
    habit = Habit(name=habit_name, user_id=user_id, completed_dates=json.dumps([]), streak=0)
    db.session.add(habit)
    db.session.commit()
    print(f"Habit '{habit_name}' added for user id {user_id}.")
    return habit

def complete_habit(habit_id):
    habit = Habit.query.get(habit_id)
    if not habit:
        print("Habit not found.")
        return

    today_str = date.today().isoformat()
    
    # Load the completed dates from JSON
    completed_dates = json.loads(habit.completed_dates or "[]")
    
    if today_str in completed_dates:
        print(f"Habit '{habit.name}' already marked complete today.")
        return

    # Add today's completion
    completed_dates.append(today_str)
    completed_dates.sort()  # optional
    habit.completed_dates = json.dumps(completed_dates)

    # Update streak
    yesterday = date.today() - timedelta(days=1)
    yesterday_str = yesterday.isoformat()
    if completed_dates[-2:] == [yesterday_str, today_str] or (habit.streak == 0):
        habit.streak += 1
    else:
        habit.streak = 1  # reset if missed a day

    db.session.commit()
    print(f"Habit '{habit.name}' marked complete! Current streak: {habit.streak} days.")

def list_user_habits(user_id):
    user = User.query.get(user_id)
    if not user:
        print("User not found.")
        return []

    habits = Habit.query.filter_by(user_id=user.id).all()
    print(f"Habits for {user.username}:")
    for h in habits:
        completed_dates = json.loads(h.completed_dates or "[]")
        status = "✅" if date.today().isoformat() in completed_dates else "❌"
        print(f"- {h.name} ({status}), Current streak: {h.streak} days")
    return habits
