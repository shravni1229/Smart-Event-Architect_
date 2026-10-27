import sqlite3
import os
from flask import g
from config import Config

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            Config.DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        # Enable foreign key constraint support in SQLite
        g.db.execute("PRAGMA foreign_keys = ON;")
    return g.db

def close_db(e=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    """Convenience helper to query database and fetch rows as dictionaries."""
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    """Executes an INSERT/UPDATE/DELETE query and commits the transaction, returning lastrowid."""
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id

def init_db_schema():
    """Initializes the database schema using schema.sql."""
    db_path = Config.DATABASE
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    
    conn = sqlite3.connect(db_path)
    with open(schema_path, mode='r', encoding='utf-8') as f:
        conn.cursor().executescript(f.read())
    conn.commit()
    conn.close()
