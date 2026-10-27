# ✨ Smart Event Architect & Recommendation System

A beginner-friendly, complete BCA Mini Project developed using **Python, Flask, SQLite / MySQL Workbench, HTML5, CSS3, and JavaScript**.

The system features a **Purple, Pink, and White responsive theme** and delivers an end-to-end event planning pipeline with an intelligent, explainable rule-based recommendation engine for budgeting and vendor service selection.

---

## 🎯 Key Project Features

### 👤 User Panel
1. **User Registration & Secure Login**: Password hashing using `werkzeug.security` (`scrypt`) and session management.
2. **Submit Event Requests**: Enter event title, event type (Wedding, Birthday, Corporate, College Fest, etc.), date, guest count, target budget, and venue location.
3. **Smart Rule-Based Service Recommendations**: Real-time service package suggestions (Catering, Stage Decor, Photography, Sound/DJ, Anchor, Coordination) with estimated costs.
4. **View Final Event Blueprint**: View the official event blueprint crafted by the administrator with itemized cost breakdown, venue suggestion, decor theme, timeline, and print option.
5. **Real-time Request Status Tracking**: Track workflow statuses: `Pending` ➔ `In Review` ➔ `Plan Created` ➔ `Confirmed` ➔ `Completed`.

### 🛡️ Admin Panel
1. **Separate Admin Authentication**: Dedicated login portal with secure password verification.
2. **Interactive Admin Dashboard**: Real-time metric cards showing Total Requests, Pending Requests, Plans Created, and Pipeline Budget.
3. **Request Inspection & Status Management**: Search and filter user requests, inspect client contact details, and update statuses.
4. **Bespoke Event Plan Builder**:
   - Pre-populated with baseline recommendations from the Python recommendation engine.
   - Select services with checkboxes and customize itemized costs.
   - Dynamic real-time total cost calculation and budget variance tracking.
   - Enter venue recommendations, color theme concepts, and schedule milestones.
   - Save blueprint directly to the database and publish to the client.
5. **Edit & Revise Blueprints**: Update existing plans anytime as vendor requirements change.

### 🧠 Recommendation Engine (`recommender.py`)
- **Budget Tier Classification**:
  - `Economy`: Budget < ₹50,000
  - `Standard`: Budget ₹50,000 – ₹1,99,999
  - `Premium`: Budget ₹2,00,000 – ₹4,99,999
  - `Luxury`: Budget ≥ ₹5,00,000
- **Feasibility Benchmark**: Calculates `per_guest = budget / guest_count` and compares against hospitality standards.
- **Explainable Weighted Allocation**: Mathematically divides budget across essential pillars (Catering ~40%, Decor ~18%, Media ~12%, Audio/DJ ~8%, Host/Coordinator ~10%, Buffer ~5-10%).
- **Curated Theme & Pro Tips**: Suggests color schemes and cost-saving advisory tips.

---

## 💻 Tech Stack & Architecture

- **Backend**: Python 3.10+ & Flask 3.x
- **Database**: 
  - **SQLite** (`event_architect.db`): Zero-configuration default database (runs out of the box anywhere).
  - **MySQL Workbench** (`schema_mysql.sql`): Importable SQL script ready for MySQL Workbench schemas, tables, and E-R diagrams.
- **Frontend**: HTML5, Modern CSS3 (Purple & Pink Palette, Glassmorphism, CSS Grid & Flexbox), Vanilla JavaScript (AJAX debounced simulator, search/filters, live blueprint printer).
- **Security**: Werkzeug password hashing, session cookies, route protection decorators (`@login_required`, `@admin_required`).

---

## 📂 Project Structure

```text
Smart_Event_Architect_Mini/
│
├── app.py                      # Main Flask web application & routes
├── config.py                   # Centralized configuration & settings
├── database.py                 # SQLite database helper functions
├── init_db.py                  # Database initialization & sample seeding
├── recommender.py              # Rule-based recommendation algorithm
├── requirements.txt            # Python dependencies (Flask, Werkzeug)
├── run.bat                     # 1-Click Windows execution script
├── schema.sql                  # SQLite relational schema
├── schema_mysql.sql            # MySQL Workbench import script
├── README.md                   # Complete documentation & viva guide
│
├── static/
│   ├── css/
│   │   └── style.css           # Purple, pink, white theme stylesheet
│   └── js/
│       ├── main.js             # Navigation, alerts, search filter, print
│       └── recommendations.js  # Live AJAX recommendation engine preview
│
└── templates/
    ├── base.html               # Base layout with navbar and footer
    ├── index.html              # Hero landing page & quick simulator
    ├── login.html              # Client login page
    ├── register.html           # Client registration page
    ├── user_dashboard.html     # User panel & request status list
    ├── new_request.html        # Event request form with live recommendations
    ├── request_details.html    # Request inspect & Admin blueprint view
    ├── services.html           # Packages & budget tier breakdown
    ├── about.html              # Project architecture & algorithm overview
    ├── 404.html                # Custom 404 error page
    └── admin/
        ├── login.html          # Dedicated Admin portal login
        ├── dashboard.html      # Admin dashboard with metrics & requests table
        ├── view_request.html   # Admin request review & status updater
        ├── create_plan.html    # Interactive plan creator & cost calculator
        └── edit_plan.html      # Modify existing blueprint
```

---

## 🚀 Windows Setup Instructions (Step-by-Step)

### Option 1: Fast 1-Click Launch (Recommended)
Simply double-click the **`run.bat`** file inside the project directory!
It will automatically:
1. Verify Python is installed.
2. Initialize the SQLite database and seed demo data.
3. Start the Flask server at `http://127.0.0.1:5000`.

---

### Option 2: Manual Command Line Setup

1. **Open PowerShell or Command Prompt** and navigate to the project directory:
   ```powershell
   cd "c:\Users\Dell\OneDrive\Desktop\Smart_Event_Architect_Mini"
   ```

2. **Install Required Packages**:
   ```powershell
   python -m pip install -r requirements.txt
   ```

3. **Initialize the SQLite Database**:
   ```powershell
   python init_db.py
   ```
   *This creates `event_architect.db` and populates sample Admin, Client users, event requests, and blueprints.*

4. **Run the Flask Application**:
   ```powershell
   python app.py
   ```

5. **Open in Web Browser**:
   Navigate to:
   ```text
   http://127.0.0.1:5000
   ```

---

## 🔑 Default Login Credentials

| Role | Email | Password | Access Level |
|---|---|---|---|
| **Administrator** | `admin@eventarchitect.com` | `admin123` | Full access to Admin Dashboard, Plan Builder, Status controls |
| **Demo Client 1** | `rohit@example.com` | `user123` | User Dashboard, Wedding Request (Plan Created), Corporate Meet |
| **Demo Client 2** | `sneha@example.com` | `user123` | User Dashboard, 21st Birthday Bash (Pending Request) |

*(You can also register any new user account using the Register page.)*

---

## 🐬 Using with MySQL Workbench

The project runs natively on **SQLite** for zero-setup execution. However, if your college or examiner requires **MySQL Workbench**:

1. Open **MySQL Workbench**.
2. Connect to your local MySQL Server (`localhost:3306`).
3. Click **File ➔ Open SQL Script...** and select `schema_mysql.sql` from this project folder.
4. Click the **Execute (Lightning Icon) ⚡** button to run the script.
5. In the **SCHEMAS** panel on the left, right-click and choose **Refresh All**. You will see the new database `smart_event_architect` with:
   - `users`
   - `event_requests`
   - `event_plans`
   - `recommendation_logs`
6. To generate the **E-R Diagram** in MySQL Workbench:
   - Go to top menu: **Database ➔ Reverse Engineer...**
   - Click **Next ➔ Next**, select `smart_event_architect`, and click **Finish**.
   - MySQL Workbench will automatically draw the visual Entity-Relationship Diagram!

---

## 🎓 BCA Viva Questions & Answers (For Project Defense)

**Q1: Why did you choose Flask instead of Django for this project?**  
*Answer:* Flask is a lightweight micro-framework that is easy to understand, modular, and does not carry heavy boilerplate. For a BCA mini project, Flask allows us to write clear routes, custom SQL queries, and clean MVC templates without unnecessary complexity.

**Q2: How does the Recommendation System work? Is it AI or Rule-Based?**  
*Answer:* It is a rule-based expert recommendation engine. It takes the user's event type, total budget, and guest count, determines the budget tier (Economy, Standard, Premium, Luxury), assesses per-guest feasibility against hospitality benchmarks, and mathematically calculates the optimal cost distribution across core services (catering, decor, media, audio/lighting, coordination).

**Q3: How are passwords stored securely?**  
*Answer:* Passwords are never stored in plain text. We use `werkzeug.security.generate_password_hash` which generates a salted cryptographic hash using the `scrypt` algorithm. When logging in, `check_password_hash` verifies the hash.

**Q4: How are admin routes protected from regular users?**  
*Answer:* We implemented Python function decorators (`@login_required` and `@admin_required`) using `functools.wraps`. The decorator checks `session['role'] == 'admin'` before allowing the view function to execute. If a normal user tries to navigate to `/admin/dashboard`, they are redirected with an alert.

**Q5: What is the relationship between the database tables?**  
*Answer:* 
- `users` (1) to `event_requests` (Many): One client can submit multiple event requests.
- `event_requests` (1) to `event_plans` (1): Each request has one unique finalized plan (`request_id UNIQUE FOREIGN KEY`).
- `users` (Admin) to `event_plans` (Many): An administrator can create multiple event blueprints.
