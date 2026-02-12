from app.db.database import get_connection

def add_assignment(text):
    # TEMP: simple parsing
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO assignments (title, deadline) VALUES (?, ?)",
        ("New Assignment", "TBD")
    )
    conn.commit()

    return "✅ Assignment added successfully."
