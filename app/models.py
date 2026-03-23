from app import db

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user = db.relationship("User", back_populates="tasks")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    tasks = db.relationship("Task", back_populates="user", cascade="all, delete-orphan")


def create_user(username, password_hash):
    user = User(username=username, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()