from flask import Blueprint, request, jsonify
from .controllers import register_user, login_user, create_task, get_tasks, update_task, delete_task
from .utils import token_required
from flask import current_app as app

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    return 'Welcome to the Task Manager API!'

@views.route('/register', methods=['POST'])
def register():
    data = request.json
    return register_user(data)

@views.route('/login', methods=['POST'])
def login():
    data = request.json
    return login_user(data, app.config['SECRET_KEY'])

@views.route('/tasks', methods=['GET', 'POST'])
@token_required
def tasks(current_user):
    if request.method == 'POST':
        data = request.json
        return create_task(current_user['id'], data)
    return get_tasks(current_user['id'])

@views.route('/tasks/<int:task_id>', methods=['PUT', 'DELETE'])
@token_required
def task_detail(current_user, task_id):
    if request.method == 'PUT':
        data = request.json
        return update_task(task_id, current_user['id'], data)
    return delete_task(task_id, current_user['id'])
