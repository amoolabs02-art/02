import os
import psycopg2

DB_URL = os.environ.get("DATABASE_URL")
DESKTOP_ID = os.environ.get("DESKTOP_ID", "desktop")


def ensure_tables(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS session_state (
            key   TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_files (
            id         SERIAL PRIMARY KEY,
            filename   TEXT NOT NULL,
            url        TEXT,
            content_b64 TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS service_log (
            id         SERIAL PRIMARY KEY,
            service    TEXT,
            event      TEXT,
            ts         TIMESTAMP DEFAULT NOW()
        )
    """)


def main():
    if not DB_URL:
        print("DATABASE_URL not set, skipping.")
        return
    try:
        conn = psycopg2.connect(DB_URL)
        conn.autocommit = False
        cur = conn.cursor()
        ensure_tables(cur)
        cur.execute(
            "INSERT INTO service_log (service, event) VALUES (%s, %s)",
            (f"desktop-{DESKTOP_ID}", "startup"),
        )
        conn.commit()
        cur.close()
        conn.close()
        print("DB ready.")
    except Exception as e:
        print(f"DB warning: {e} — continuing without DB.")


if __name__ == "__main__":
    main()
