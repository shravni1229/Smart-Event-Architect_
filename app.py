import os
import json
from functools import wraps
from datetime import datetime
from flask import (
    Flask, render_template, request, redirect,
    url_for, session, flash, jsonify, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from database import get_db, close_db, query_db, execute_db
from recommender import recommend_services, classify_budget_tier

app = Flask(__name__)
app.config.from_object(Config)

# Register database teardown
app.teardown_appcontext(close_db)

# Ensure database exists upon application start
with app.app_context():
    if not os.path.exists(Config.DATABASE):
        from init_db import init_db
        init_db()

# Global template context variables
@app.context_processor
def inject_globals():
    return {
        'current_year': datetime.now().year,
        'currency_symbol': Config.CURRENCY_SYMBOL,
        'event_types': Config.EVENT_TYPES,
        'status_options': Config.STATUS_OPTIONS
    }

# ==========================================================
# Authentication & Role Decorators
# ==========================================================
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please sign in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Administrative credentials required.', 'warning')
            return redirect(url_for('admin_login', next=request.url))
        if session.get('role') != 'admin':
            flash('Access restricted to administrators.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ==========================================================
# Public Routes
# ==========================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/services')
def services_page():
    return render_template('services.html')

@app.route('/about')
def about_page():
    return render_template('about.html')

# ==========================================================
# Authentication Routes
# ==========================================================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not email or not password:
            flash('Please complete all required fields.', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match. Please verify.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must contain at least 6 characters.', 'danger')
            return render_template('register.html')

        existing_user = query_db("SELECT id FROM users WHERE email = ?", (email,), one=True)
        if existing_user:
            flash('An account with this email already exists. Please sign in.', 'warning')
            return redirect(url_for('login'))

        password_hash = generate_password_hash(password)
        user_id = execute_db("""
            INSERT INTO users (full_name, email, phone, password_hash, role)
            VALUES (?, ?, ?, ?, 'user')
        """, (full_name, email, phone, password_hash))

        session['user_id'] = user_id
        session['full_name'] = full_name
        session['email'] = email
        session['role'] = 'user'

        flash(f'Account created successfully! Welcome to Smart Event Architect, {full_name}.', 'success')
        return redirect(url_for('user_dashboard'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('user_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = query_db("SELECT * FROM users WHERE email = ?", (email,), one=True)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            session['email'] = user['email']
            session['role'] = user['role']

            flash(f'Welcome back, {user["full_name"]}!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('user_id') and session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = query_db("SELECT * FROM users WHERE email = ? AND role = 'admin'", (email,), one=True)

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            session['email'] = user['email']
            session['role'] = 'admin'

            flash(f'Admin authentication successful. Welcome, {user["full_name"]}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid administrator credentials or access denied.', 'danger')

    return render_template('admin/login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

# ==========================================================
# User Panel Routes
# ==========================================================
@app.route('/dashboard')
@login_required
def user_dashboard():
    user_id = session['user_id']
    requests = query_db("""
        SELECT * FROM event_requests
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    return render_template('user_dashboard.html', requests=requests)

@app.route('/request/new', methods=['GET', 'POST'])
@login_required
def new_request():
    if request.method == 'POST':
        event_title = request.form.get('event_title', '').strip()
        event_type = request.form.get('event_type', '').strip()
        event_date = request.form.get('event_date', '').strip()
        guest_count_str = request.form.get('guest_count', '').strip()
        budget_str = request.form.get('budget', '').strip()
        location = request.form.get('location', '').strip()
        special_notes = request.form.get('special_notes', '').strip()

        if not event_title or not event_type or not event_date or not guest_count_str or not budget_str or not location:
            flash('Please fill in all required event details.', 'danger')
            return render_template('new_request.html')

        try:
            guest_count = int(guest_count_str)
            budget = float(budget_str)
            if guest_count <= 0 or budget <= 0:
                raise ValueError()
        except ValueError:
            flash('Please enter valid positive numbers for guests and budget.', 'danger')
            return render_template('new_request.html')

        user_id = session['user_id']
        req_id = execute_db("""
            INSERT INTO event_requests 
            (user_id, event_title, event_type, event_date, guest_count, budget, location, special_notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
        """, (user_id, event_title, event_type, event_date, guest_count, budget, location, special_notes))

        # Log recommendation generation
        try:
            recom = recommend_services(event_type, budget, guest_count)
            tier = recom['budget_tier']
            services_json = json.dumps(recom['recommended_services'])
            execute_db("""
                INSERT INTO recommendation_logs
                (request_id, event_type, budget, guest_count, budget_tier, recommended_services_json)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (req_id, event_type, budget, guest_count, tier, services_json))
        except Exception as e:
            app.logger.warning(f"Could not log recommendation: {e}")

        flash('Event request submitted successfully! Our architects will design your custom plan.', 'success')
        return redirect(url_for('view_request_details', request_id=req_id))

    return render_template('new_request.html')

@app.route('/request/<int:request_id>')
@login_required
def view_request_details(request_id):
    req = query_db("SELECT * FROM event_requests WHERE id = ?", (request_id,), one=True)
    if not req:
        flash('Event request not found.', 'danger')
        return redirect(url_for('user_dashboard'))

    # Access check: user owns request OR user is admin
    if req['user_id'] != session['user_id'] and session.get('role') != 'admin':
        flash('Unauthorized access to this event request.', 'danger')
        return redirect(url_for('user_dashboard'))

    # Fetch event plan if created by admin
    plan = query_db("SELECT * FROM event_plans WHERE request_id = ?", (request_id,), one=True)
    admin_user = None
    plan_services = []
    plan_costs = {}

    if plan:
        admin_user = query_db("SELECT full_name, email FROM users WHERE id = ?", (plan['admin_id'],), one=True)
        try:
            plan_services = json.loads(plan['services_included'])
        except Exception:
            plan_services = []
        try:
            plan_costs = json.loads(plan['cost_breakdown'])
        except Exception:
            plan_costs = {}

    # Generate system recommendations for reference
    recommendations = recommend_services(req['event_type'], req['budget'], req['guest_count'])

    return render_template(
        'request_details.html',
        req=req,
        plan=plan,
        admin_user=admin_user,
        plan_services=plan_services,
        plan_costs=plan_costs,
        recommendations=recommendations
    )

# ==========================================================
# Admin Panel Routes
# ==========================================================
@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Overall summary metrics
    total_req_row = query_db("SELECT COUNT(*) AS cnt FROM event_requests", one=True)
    total_requests = total_req_row['cnt'] if total_req_row else 0

    pending_req_row = query_db("SELECT COUNT(*) AS cnt FROM event_requests WHERE status IN ('Pending', 'In Review')", one=True)
    pending_requests = pending_req_row['cnt'] if pending_req_row else 0

    plans_row = query_db("SELECT COUNT(*) AS cnt FROM event_plans", one=True)
    plans_created = plans_row['cnt'] if plans_row else 0

    budget_row = query_db("SELECT SUM(budget) AS total_b FROM event_requests", one=True)
    total_budget = budget_row['total_b'] or 0

    # Fetch all requests with user details and plan status
    requests = query_db("""
        SELECT 
            r.*,
            u.full_name AS client_name,
            u.email AS client_email,
            u.phone AS client_phone,
            p.id AS plan_id
        FROM event_requests r
        JOIN users u ON r.user_id = u.id
        LEFT JOIN event_plans p ON r.id = p.request_id
        ORDER BY r.created_at DESC
    """)

    return render_template(
        'admin/dashboard.html',
        total_requests=total_requests,
        pending_requests=pending_requests,
        plans_created=plans_created,
        total_budget=total_budget,
        requests=requests
    )

@app.route('/admin/request/<int:request_id>')
@admin_required
def admin_view_request(request_id):
    req = query_db("SELECT * FROM event_requests WHERE id = ?", (request_id,), one=True)
    if not req:
        flash('Request not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    client = query_db("SELECT * FROM users WHERE id = ?", (req['user_id'],), one=True)
    plan = query_db("SELECT * FROM event_plans WHERE request_id = ?", (request_id,), one=True)
    recommendations = recommend_services(req['event_type'], req['budget'], req['guest_count'])

    return render_template(
        'admin/view_request.html',
        req=req,
        client=client,
        plan=plan,
        recommendations=recommendations
    )

@app.route('/admin/request/<int:request_id>/status', methods=['POST'])
@admin_required
def admin_update_status(request_id):
    new_status = request.form.get('status', '').strip()
    if new_status in Config.STATUS_OPTIONS:
        execute_db("UPDATE event_requests SET status = ? WHERE id = ?", (new_status, request_id))
        flash(f'Request #{request_id} status updated to "{new_status}".', 'success')
    else:
        flash('Invalid status selected.', 'danger')
    return redirect(url_for('admin_view_request', request_id=request_id))

@app.route('/admin/request/<int:request_id>/create-plan', methods=['GET', 'POST'])
@admin_required
def admin_create_plan(request_id):
    req = query_db("SELECT * FROM event_requests WHERE id = ?", (request_id,), one=True)
    if not req:
        flash('Request not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    client = query_db("SELECT * FROM users WHERE id = ?", (req['user_id'],), one=True)
    existing_plan = query_db("SELECT id FROM event_plans WHERE request_id = ?", (request_id,), one=True)
    if existing_plan:
        flash('A plan already exists for this request. You can edit it below.', 'info')
        return redirect(url_for('admin_edit_plan', request_id=request_id))

    recommendations = recommend_services(req['event_type'], req['budget'], req['guest_count'])

    if request.method == 'POST':
        plan_title = request.form.get('plan_title', '').strip()
        description = request.form.get('description', '').strip()
        venue_suggestion = request.form.get('venue_suggestion', '').strip()
        decor_theme = request.form.get('decor_theme', '').strip()
        timeline_summary = request.form.get('timeline_summary', '').strip()
        admin_notes = request.form.get('admin_notes', '').strip()
        status = request.form.get('status', 'Plan Created').strip()

        # Extract selected services and their costs
        service_indexes = request.form.getlist('service_include')
        services_included = []
        cost_breakdown = {}
        total_estimated_cost = 0.0

        for idx in service_indexes:
            svc_name = request.form.get(f'service_name_{idx}', '').strip()
            svc_cost_str = request.form.get(f'service_cost_{idx}', '0').strip()
            if svc_name:
                try:
                    cost_val = float(svc_cost_str)
                except ValueError:
                    cost_val = 0.0
                services_included.append(svc_name)
                cost_breakdown[svc_name] = cost_val
                total_estimated_cost += cost_val

        if not plan_title or not description or not services_included:
            flash('Please provide plan title, description, and at least one service.', 'danger')
            return render_template('admin/create_plan.html', req=req, client=client, recommendations=recommendations)

        admin_id = session['user_id']
        execute_db("""
            INSERT INTO event_plans 
            (request_id, admin_id, plan_title, description, services_included, cost_breakdown, total_estimated_cost, venue_suggestion, decor_theme, timeline_summary, admin_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            request_id,
            admin_id,
            plan_title,
            description,
            json.dumps(services_included),
            json.dumps(cost_breakdown),
            total_estimated_cost,
            venue_suggestion,
            decor_theme,
            timeline_summary,
            admin_notes
        ))

        # Update request status
        execute_db("UPDATE event_requests SET status = ? WHERE id = ?", (status, request_id))

        flash(f'Event Plan "{plan_title}" created successfully and published to {client["full_name"]}!', 'success')
        return redirect(url_for('admin_view_request', request_id=request_id))

    return render_template(
        'admin/create_plan.html',
        req=req,
        client=client,
        recommendations=recommendations
    )

@app.route('/admin/request/<int:request_id>/edit-plan', methods=['GET', 'POST'])
@admin_required
def admin_edit_plan(request_id):
    req = query_db("SELECT * FROM event_requests WHERE id = ?", (request_id,), one=True)
    if not req:
        flash('Request not found.', 'danger')
        return redirect(url_for('admin_dashboard'))

    client = query_db("SELECT * FROM users WHERE id = ?", (req['user_id'],), one=True)
    plan = query_db("SELECT * FROM event_plans WHERE request_id = ?", (request_id,), one=True)
    if not plan:
        flash('No plan found for this request. Please create one.', 'warning')
        return redirect(url_for('admin_create_plan', request_id=request_id))

    try:
        plan_costs = json.loads(plan['cost_breakdown'])
    except Exception:
        plan_costs = {}

    if request.method == 'POST':
        plan_title = request.form.get('plan_title', '').strip()
        description = request.form.get('description', '').strip()
        venue_suggestion = request.form.get('venue_suggestion', '').strip()
        decor_theme = request.form.get('decor_theme', '').strip()
        timeline_summary = request.form.get('timeline_summary', '').strip()
        admin_notes = request.form.get('admin_notes', '').strip()
        status = request.form.get('status', 'Plan Created').strip()

        # Extract selected services and their costs
        service_indexes = request.form.getlist('service_include')
        services_included = []
        cost_breakdown = {}
        total_estimated_cost = 0.0

        for idx in service_indexes:
            svc_name = request.form.get(f'service_name_{idx}', '').strip()
            svc_cost_str = request.form.get(f'service_cost_{idx}', '0').strip()
            if svc_name:
                try:
                    cost_val = float(svc_cost_str)
                except ValueError:
                    cost_val = 0.0
                services_included.append(svc_name)
                cost_breakdown[svc_name] = cost_val
                total_estimated_cost += cost_val

        if not plan_title or not description or not services_included:
            flash('Please provide plan title, description, and at least one service.', 'danger')
            return render_template('admin/edit_plan.html', req=req, client=client, plan=plan, plan_costs=plan_costs)

        execute_db("""
            UPDATE event_plans 
            SET plan_title = ?, description = ?, services_included = ?, cost_breakdown = ?,
                total_estimated_cost = ?, venue_suggestion = ?, decor_theme = ?,
                timeline_summary = ?, admin_notes = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            plan_title,
            description,
            json.dumps(services_included),
            json.dumps(cost_breakdown),
            total_estimated_cost,
            venue_suggestion,
            decor_theme,
            timeline_summary,
            admin_notes,
            plan['id']
        ))

        # Update request status
        execute_db("UPDATE event_requests SET status = ? WHERE id = ?", (status, request_id))

        flash(f'Plan "{plan_title}" updated successfully!', 'success')
        return redirect(url_for('admin_view_request', request_id=request_id))

    return render_template(
        'admin/edit_plan.html',
        req=req,
        client=client,
        plan=plan,
        plan_costs=plan_costs
    )

# ==========================================================
# API Endpoints (For Dynamic AJAX Client Calculations)
# ==========================================================
@app.route('/api/recommend')
def api_recommend():
    event_type = request.args.get('event_type', '').strip()
    try:
        budget = float(request.args.get('budget', 0))
        guest_count = int(request.args.get('guest_count', 1))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid budget or guest_count parameters.'}), 400

    if not event_type or budget <= 0 or guest_count <= 0:
        return jsonify({'error': 'event_type, budget and guest_count must be valid.'}), 400

    data = recommend_services(event_type, budget, guest_count)
    return jsonify(data)

# ==========================================================
# Error Handlers
# ==========================================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ==========================================================
# Application Entry Point
# ==========================================================
if __name__ == '__main__':
    print("==================================================")
    print("✨ Smart Event Architect & Recommendation System")
    print("Server running locally at: http://127.0.0.1:5000")
    print("==================================================")
    app.run(debug=True, host='127.0.0.1', port=5000)
