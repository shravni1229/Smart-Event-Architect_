"""
Database Initialization Script for Smart Event Architect.
Creates SQLite tables and seeds sample Administrator and User records.
"""

import os
import json
import sqlite3
from werkzeug.security import generate_password_hash
from config import Config

def init_db():
    db_path = Config.DATABASE
    
    # If old DB exists, we can re-create or ensure tables exist
    print(f"[*] Initializing database at: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    
    cursor = conn.cursor()
    
    # Check if admin already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (Config.ADMIN_DEFAULT_EMAIL,))
    admin_exists = cursor.fetchone()
    
    if not admin_exists:
        print("[+] Creating default Admin account...")
        admin_hash = generate_password_hash(Config.ADMIN_DEFAULT_PASSWORD)
        cursor.execute("""
            INSERT INTO users (full_name, email, phone, password_hash, role)
            VALUES (?, ?, ?, ?, ?)
        """, (
            Config.ADMIN_DEFAULT_NAME,
            Config.ADMIN_DEFAULT_EMAIL,
            '+91 9876543210',
            admin_hash,
            'admin'
        ))
        admin_id = cursor.lastrowid
    else:
        admin_id = admin_exists[0]
        
    # Check if sample users exist
    cursor.execute("SELECT id FROM users WHERE email = ?", ('rohit@example.com',))
    user_exists = cursor.fetchone()
    
    if not user_exists:
        print("[+] Creating sample client users...")
        user_hash = generate_password_hash('user123')
        
        cursor.execute("""
            INSERT INTO users (full_name, email, phone, password_hash, role)
            VALUES (?, ?, ?, ?, ?)
        """, ('Rohit Sharma', 'rohit@example.com', '+91 9123456789', user_hash, 'user'))
        user1_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO users (full_name, email, phone, password_hash, role)
            VALUES (?, ?, ?, ?, ?)
        """, ('Sneha Patil', 'sneha@example.com', '+91 9876501234', user_hash, 'user'))
        user2_id = cursor.lastrowid

        print("[+] Seeding sample event requests...")
        # Request 1: Rohit's Wedding (Has a created plan)
        cursor.execute("""
            INSERT INTO event_requests 
            (user_id, event_title, event_type, event_date, guest_count, budget, location, special_notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user1_id,
            'Grand Silver Jubilee Wedding & Reception',
            'Wedding Ceremony & Reception',
            '2026-12-15',
            250,
            450000.00,
            'The Corinthians Resort, Pune',
            'Royal purple and soft blush pink decor theme. Prefer acoustic music during family dinner.',
            'Plan Created'
        ))
        req1_id = cursor.lastrowid

        # Request 2: Sneha's Birthday (Pending)
        cursor.execute("""
            INSERT INTO event_requests 
            (user_id, event_title, event_type, event_date, guest_count, budget, location, special_notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user2_id,
            "Sneha's 21st Celestial Birthday Bash",
            'Birthday Celebration',
            '2026-11-20',
            60,
            85000.00,
            'Bandra Banquet & Lounge, Mumbai',
            'Neon balloon backdrop, personalized cake cutting ceremony, and upbeat dance DJ.',
            'Pending'
        ))
        req2_id = cursor.lastrowid

        # Request 3: Rohit's Corporate Meet (In Review)
        cursor.execute("""
            INSERT INTO event_requests 
            (user_id, event_title, event_type, event_date, guest_count, budget, location, special_notes, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user1_id,
            'TechCorp Annual Leadership Meet',
            'Corporate Conference & Seminar',
            '2027-01-10',
            120,
            200000.00,
            'Hinjawadi IT Park Convention Center, Pune',
            'Dual projection screens, high-tea, continuous coffee station, and keynote speaker audio.',
            'In Review'
        ))

        print("[+] Creating sample event plan for Request #1...")
        services_list = [
            "Catering & Dining Hospitality",
            "Theme Decor & Stage Styling",
            "Photography & Video Memories",
            "Sound, DJ & Intelligent Lighting",
            "Anchor / Emcee & Guest Engagement",
            "On-Site Event Coordinator"
        ]
        costs = {
            "Catering & Dining Hospitality": 190000,
            "Theme Decor & Stage Styling": 90000,
            "Photography & Video Memories": 63000,
            "Sound, DJ & Intelligent Lighting": 45000,
            "Anchor / Emcee & Guest Engagement": 22500,
            "On-Site Event Coordinator": 22500
        }
        timeline = (
            "04:00 PM - Guest Arrival & Floral Welcome Mocktails\n"
            "05:30 PM - Ring Exchange & Traditional Ceremony on Floral Stage\n"
            "07:30 PM - Live Sangeet & Couple Performance on LED Dance Floor\n"
            "08:30 PM - Multi-Cuisine Royal Banquet Opens\n"
            "10:30 PM - Celebration Cake Cutting & Photo Session"
        )
        cursor.execute("""
            INSERT INTO event_plans
            (request_id, admin_id, plan_title, description, services_included, cost_breakdown, total_estimated_cost, venue_suggestion, decor_theme, timeline_summary, admin_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            req1_id,
            admin_id,
            'Royal Orchid Grand Wedding Blueprint',
            'A comprehensive end-to-end wedding package designed specifically to Rohit & family requirements. Featuring luxury floral mandap, four-course gourmet buffet, drone photography, and dedicated floor coordination.',
            json.dumps(services_list),
            json.dumps(costs),
            433000.00,
            'The Corinthians Resort & Club / Orchid Grand Lawn, Pune',
            'Royal Orchid Purple & Blush Pink with Grand Chandeliers',
            timeline,
            'Estimated budget fits well within the client limit of Rs. 4,50,000 with a safety buffer of Rs. 17,000. Catering tasting scheduled 3 weeks prior.'
        ))

    conn.commit()
    conn.close()
    print("[OK] Database initialized successfully!")
    print("--------------------------------------------------")
    print("Default Admin Credentials:")
    print(f"  Email:    {Config.ADMIN_DEFAULT_EMAIL}")
    print(f"  Password: {Config.ADMIN_DEFAULT_PASSWORD}")
    print("Default User Credentials:")
    print("  Email:    rohit@example.com")
    print("  Password: user123")
    print("--------------------------------------------------")

if __name__ == '__main__':
    init_db()
