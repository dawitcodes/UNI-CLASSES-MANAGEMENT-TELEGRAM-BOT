from app.db.database import get_connection

def read_assignments():
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT title, deadline FROM assignments"
    ).fetchall()

    if not rows:
        return "📭 No assignments yet."

    return "\n".join([f"📌 {t} — due {d}" for t, d in rows])


def read_schedule():
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT day, subject, time FROM schedule"
    ).fetchall()

    if not rows:
        return "📅 No schedule available yet."

    return "\n".join([f"📘 {day}: {subject} at {time}" for day, subject, time in rows])


def read_instructors():
    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT name, contact FROM instructors"
    ).fetchall()

    if not rows:
        return "👨‍🏫 Instructor contact info not available yet."

    return "\n".join([f"👤 {name}: {contact}" for name, contact in rows])

