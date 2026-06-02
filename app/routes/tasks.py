from flask import Blueprint,render_template,redirect,request,url_for,flash,session
from app import db
from app.models import Task

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/')
def view_tasks():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    tasks =  Task.query.filter_by(user_id=session['user']).all()

    return render_template('task.html', tasks=tasks)


@tasks_bp.route('/add', methods=['POST'])
def add_task():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    title = request.form.get('title')

    if title:
        new_task = Task(title=title, status='Pending', user_id=session['user'])
        db.session.add(new_task)
        db.session.commit()

        flash('Task added successfully', 'success')

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_status(task_id):
    task = Task.query.filter_by(id=task_id,user_id=session['user']).first()

    if task:
        if task.status == 'Pending':
            task.status = 'Working'

        elif task.status == 'Working':
            task.status = 'Done'

        else:
            task.status = 'Pending'

        db.session.commit()

    return redirect(url_for('tasks.view_tasks'))


@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():
    Task.query.filter_by(user_id=session['user']).delete()

    db.session.commit()

    flash('All tasks cleared!', 'info')

    return redirect(url_for('tasks.view_tasks'))
