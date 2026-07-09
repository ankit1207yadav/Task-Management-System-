import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import initialize_database, verify_admin_credentials, fetch_all_tasks, update_task_status
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Configure application secret key (uses environment variable with fallback)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_session_secret_key_12345")

# Run database setup check during application start
with app.app_context():
    initialize_database()

@app.route('/', methods=['GET', 'POST'])
def login():
    """
    Handles administrator authentication.
    """
    # If the administrator is already authenticated, redirect straight to the dashboard
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        admin_id = request.form.get('admin_id', '').strip()
        password = request.form.get('password', '').strip()

        # Form validation check
        if not admin_id or not password:
            flash('Please enter both Admin ID and Password.', 'error')
            return render_template('login.html')

        # Check authentication details in the database
        admin = verify_admin_credentials(admin_id, password)

        if admin:
            session['admin_id'] = admin['admin_id']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Admin ID or Password', 'error')

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """
    Displays the admin dashboard panel and processes task completion status updates.
    """
    # Enforce session verification
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    # Handle updating task completion status
    if request.method == 'POST':
        task_title = request.form.get('task_title')
        completed_status = request.form.get('completed')

        if task_title and completed_status:
            if update_task_status(task_title, completed_status):
                flash(f'Successfully updated status for "{task_title}"!', 'success')
            else:
                flash('Failed to update task status in the database.', 'error')
        else:
            flash('Missing task title or status selection.', 'error')

    # Get updated tasks list
    tasks = fetch_all_tasks()

    # Determine current selection using request arguments, defaulting to updated task on POST or first task
    default_title = tasks[0]['task_title'] if tasks else ''
    if request.method == 'POST':
        default_title = request.form.get('task_title', default_title)
    selected_title = request.args.get('task_title', default_title)

    # Locate the target selected task object
    current_task = next(
        (t for t in tasks if t['task_title'] == selected_title),
        None
    )

    # Fallback to the first task if the requested title doesn't match
    if not current_task and tasks:
        current_task = tasks[0]

    return render_template(
        'dashboard.html',
        tasks=tasks,
        current_task=current_task
    )

@app.route('/logout')
def logout():
    """
    Terminates the session and redirects to login interface.
    """
    session.pop('admin_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Retrieve configuration settings from environment variables
    debug_mode = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)
