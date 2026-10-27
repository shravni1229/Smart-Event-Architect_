-- Smart Event Architect & Recommendation System
-- SQLite Database Schema

PRAGMA foreign_keys = ON;

-- Users Table (Stores both regular clients and administrators)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user', -- 'user' or 'admin'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event Requests Table (Submitted by clients)
CREATE TABLE IF NOT EXISTS event_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    event_title TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_date TEXT NOT NULL,
    guest_count INTEGER NOT NULL,
    budget REAL NOT NULL,
    location TEXT NOT NULL,
    special_notes TEXT,
    status TEXT NOT NULL DEFAULT 'Pending', -- 'Pending', 'In Review', 'Plan Created', 'Confirmed', 'Completed', 'Cancelled'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Event Plans Table (Created by Admin for a specific event request)
CREATE TABLE IF NOT EXISTS event_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER UNIQUE NOT NULL,
    admin_id INTEGER NOT NULL,
    plan_title TEXT NOT NULL,
    description TEXT NOT NULL,
    services_included TEXT NOT NULL, -- JSON list of services
    cost_breakdown TEXT NOT NULL,    -- JSON object: service -> cost
    total_estimated_cost REAL NOT NULL,
    venue_suggestion TEXT,
    decor_theme TEXT,
    timeline_summary TEXT,
    admin_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES event_requests(id) ON DELETE CASCADE,
    FOREIGN KEY (admin_id) REFERENCES users(id)
);

-- Recommendation Logs Table (Stores rule-based recommendation history)
CREATE TABLE IF NOT EXISTS recommendation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER,
    event_type TEXT NOT NULL,
    budget REAL NOT NULL,
    guest_count INTEGER NOT NULL,
    budget_tier TEXT NOT NULL,
    recommended_services_json TEXT NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES event_requests(id) ON DELETE SET NULL
);
