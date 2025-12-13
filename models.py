"""
models.py
File-backed models for Habit Tracker.
"""

from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
import json
from pathlib import Path
import uuid
import datetime

# Import werkzeug functions lazily to get clearer errors if missing
try:
    from werkzeug.security import generate_password_hash, check_password_hash
except Exception as e:
    raise ImportError(
        "Missing dependency: werkzeug. Run `pip install werkzeug` in your venv. "
        f"Original error: {e}"
    )

DATA_FILE = Path("data") / "users.json"
DATA_FILE.parent.mkdir(exist_ok=True, parents=True)

def _now_iso():
    return datetime.datetime.utcnow().isoformat()

def load_data() -> Dict:
    """Load user data from JSON file."""
    if not DATA_FILE.exists():
        return {"users": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"users": []}

def save_data(data: Dict):
    """Save data dict to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@dataclass
class Habit:
    """A simple Habit model."""
    id: str
    name: str
    description: str = ""
    points: int = 1
    created_at: str = field(default_factory=_now_iso)
    completed_dates: List[str] = field(default_factory=list)

    def complete_today(self) -> bool:
        today = datetime.datetime.utcnow().date().isoformat()
        if today not in self.completed_dates:
            self.completed_dates.append(today)
            return True
        return False

@dataclass
class User:
    """A simple User model for file-backed auth."""
    id: str
    username: str
    pw_hash: str
    points: int = 0
    habits: List[Dict] = field(default_factory=list)
    created_at: str = field(default_factory=_now_iso)

    @classmethod
    def create(cls, username: str, password: str):
        uid = str(uuid.uuid4())
        pw_hash = generate_password_hash(password)
        return cls(id=uid, username=username, pw_hash=pw_hash)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.pw_hash, password)

    def add_habit(self, habit: Habit):
        self.habits.append(asdict(habit))

    def to_dict(self):
        return asdict(self)

# Storage helper functions
def find_user_by_username(username: str) -> Optional[User]:
    data = load_data()
    for u in data.get("users", []):
        if u.get("username") == username:
            return User(**u)
    return None

def find_user_by_id(user_id: str) -> Optional[User]:
    data = load_data()
    for u in data.get("users", []):
        if u.get("id") == user_id:
            return User(**u)
    return None

def save_user(user: User):
    data = load_data()
    users = data.get("users", [])
    for i, u in enumerate(users):
        if u.get("id") == user.id:
            users[i] = user.to_dict()
            data["users"] = users
            save_data(data)
            return
    users.append(user.to_dict())
    data["users"] = users
    save_data(data)

def list_users() -> List[User]:
    data = load_data()
    return [User(**u) for u in data.get("users", [])]
