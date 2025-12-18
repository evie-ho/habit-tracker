from app import app, db, User, Habit
from datetime import date

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create initial users
    users = [
        ("evie", "evie@example.com"),
        ("john", "john@example.com"),
        ("sarah", "sarah@example.com")
    ]
    for u, e in users:
        if not User.query.filter_by(username=u).first():
            db.session.add(User(username=u, email=e))
    db.session.commit()

    # Create initial habits
    habits = [
        ("Morning Run", "evie"),
        ("Read 20 Pages", "john"),
        ("Meditate", "john"),
        ("Sleep by 10 PM", "sarah")
    ]
    for h, u in habits:
        user = User.query.filter_by(username=u).first()
        if user and not Habit.query.filter_by(name=h, user_id=user.id).first():
            habit = Habit(name=h, user_id=user.id, streak=0, last_completed=None)
            db.session.add(habit)
    db.session.commit()

    print("Database initialized!")
    print("Users:", User.query.all())
    print("Habits:", Habit.query.all())
