from .models import User, Task, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
import jwt
import datetime

def register_user(data):
    username = data.get('username')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return {"message": "User already exists"}, 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered successfully"}, 201

def login_user(data, secret_key):
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                           secret_key, algorithm='HS256')
        return {"token": token}, 200
    return {"message": "Invalid credentials"}, 401

def create_task(user_id, data):
    title = data.get('title')
    description = data.get('description')
    new_task = Task(title=title, description=description, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    return {"message": "Task created successfully"}, 201

def get_tasks(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": t.id, "title": t.title, "description": t.description, "completed": t.completed} for t in tasks])

def update_task(task_id, user_id, data):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return {"message": "Task not found"}, 404
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return {"message": "Task updated successfully"}, 200

def delete_task(task_id, user_id):
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return {"message": "Task not found"}, 404
    db.session.delete(task)
    db.session.commit()
    return {"message": "Task deleted successfully"}, 200
