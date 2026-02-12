from app.services.student_service import (
    read_assignments,
    read_schedule,
    read_instructors
)
from app.services.admin_service import (
    add_assignment
)

def route(classification: dict, raw_text: str):
    role = classification["role"]
    topic = classification["topic"]
    action = classification["action"]

    # STUDENT READ
    if role == "student" and action == "read":
        if topic == "assignment":
            return read_assignments()
        if topic == "schedule":
            return read_schedule()
        if topic == "instructors_contact":
            return read_instructors()

    # ADMIN ADD
    if role == "admin" and action == "add":
        if topic == "assignment":
            return add_assignment(raw_text)

    return "⚠️ Information not available yet."
