# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import User, Habit, save_user, find_user_by_username, list_users, find_user_by_id
import uuid

app = Flask(__name__)
app.secret_key = "dev-secret-change-me"  # change in production

# -------------------
# Index Route
# -------------------
@app.route("/")
def index():
    """Home page showing welcome and links to login/register."""
    user = current_user()
    return render_template("index.html", user=user)


@app.route("/health")
def health():
    return "OK"



# -------------------
# Authentication Routes
# -------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password required.", "error")
            return redirect(url_for("register"))
        if find_user_by_username(username):
            flash("Username already taken.", "error")
            return redirect(url_for("register"))
        user = User.create(username, password)
        save_user(user)
        session["user_id"] = user.id
        flash("Account created. You're logged in.", "success")
        return redirect(url_for("index"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in a user by verifying password."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = find_user_by_username(username)
        if not user or not user.check_password(password):
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))
        session["user_id"] = user.id
        flash("Logged in successfully.", "success")
        return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log out the current user."""
    session.pop("user_id", None)
    flash("Logged out.", "info")
    return redirect(url_for("index"))


# -------------------
# Helper function
# -------------------
def current_user():
    """Return the currently logged-in user or None."""
    uid = session.get("user_id")
    if not uid:
        return None
    return find_user_by_id(uid)


# -------------------
# User switcher (for dev/testing)
# -------------------
@app.route("/users")
def show_users():
    """Show all users and allow switching for development/testing."""
    users = list_users()
    return render_template("users.html", users=users)


@app.route("/switch_user/<user_id>")
def switch_user(user_id):
    """Switch session to another user (dev/testing)."""
    user = find_user_by_id(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for("show_users"))
    session["user_id"] = user.id
    flash(f"Switched to {user.username}.", "success")
    return redirect(url_for("index"))


# -------------------
# Run app
# -------------------
if __name__ == "__main__":
    app.run(debug=True)
