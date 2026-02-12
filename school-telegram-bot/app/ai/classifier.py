# # import json
# # from openai import OpenAI
# # from app.config import OPENAI_API_KEY

# # client = OpenAI(api_key=OPENAI_API_KEY)

# # CLASSIFIER_PROMPT = """
# # You are the AI brain of a Telegram-based School Management Bot.
# # Your task is to classify a SINGLE incoming Telegram message into exactly one of these categories:
# # - materials_access
# # - schedule
# # - assignment
# # - upcoming_exams
# # - instructors_contact
# # - information
# # Or admin_add if a class rep adds data.

# # Rules:
# # - Return ONLY valid JSON, nothing else.
# # - If unclear, return intent="unknown" and other fields null.

# # JSON FORMAT:
# # {
# #   "role": "student | admin",
# #   "intent": "<topic | admin_add | unknown>",
# #   "topic": "<materials_access | schedule | assignment | upcoming_exams | instructors_contact | information | null>",
# #   "action": "<read | add | update | null>",
# #   "summary": "<short plain-English summary>"
# # }

# # EXAMPLES:

# # Message: "Any assignments due this week?"
# # Output:
# # {
# #   "role": "student",
# #   "intent": "assignment",
# #   "topic": "assignment",
# #   "action": "read",
# #   "summary": "asking about upcoming assignment deadlines"
# # }

# # Message: "How do I contact our physics instructor?"
# # Output:
# # {
# #   "role": "student",
# #   "intent": "instructors_contact",
# #   "topic": "instructors_contact",
# #   "action": "read",
# #   "summary": "requesting instructor contact details"
# # }

# # Message: "Add math exam on Feb 25 at 10 AM"
# # Output:
# # {
# #   "role": "admin",
# #   "intent": "admin_add",
# #   "topic": "upcoming_exams",
# #   "action": "add",
# #   "summary": "adding a new math exam with date and time"
# # }

# # Now classify the following message:
# # """



# # def classify_message(user_message: str):
# #     try:
# #         # Combine examples + user message in ONE user content
# #         user_content = f"""
# # Here are examples:

# # 1. "Any assignments due this week?"
# # {{"role": "student", "intent": "assignment", "topic": "assignment", "action": "read", "summary": "asking about upcoming assignment deadlines"}}

# # 2. "How do I contact our physics instructor?"
# # {{"role": "student", "intent": "instructors_contact", "topic": "instructors_contact", "action": "read", "summary": "requesting instructor contact details"}}

# # 3. "Add math exam on Feb 25 at 10 AM"
# # {{"role": "admin", "intent": "admin_add", "topic": "upcoming_exams", "action": "add", "summary": "adding a new math exam with date and time"}}

# # Now classify the following message in the same JSON format:

# # "{user_message}"
# # """

# #         response = client.chat.completions.create(
# #             model="gpt-4o-mini",
# #             messages=[
# #                 {"role": "system", "content": "You are a JSON classifier. Return ONLY JSON as specified."},
# #                 {"role": "user", "content": user_content}
# #             ],
# #             temperature=0
# #         )

# #         ai_output = response.choices[0].message.content.strip()

# #         # attempt to extract JSON if AI adds extra text
# #         if not ai_output.startswith("{"):
# #             ai_output = ai_output[ai_output.find("{"):ai_output.rfind("}")+1]

# #         return json.loads(ai_output)

# #     except Exception as e:
# #         print("CLASSIFIER ERROR:", e)
# #         return {
# #             "role": "student",
# #             "intent": "unknown",
# #             "topic": "null",
# #             "action": "null",
# #             "summary": "Error processing message"
# #         }

import json
from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

# 1. We keep the instructions in the System Prompt.
# Note: When using JSON mode, the word "JSON" must appear in the system prompt.
SYSTEM_INSTRUCTIONS = """
You are the AI brain of a Telegram-based School Management Bot.
Your task is to classify a SINGLE incoming Telegram message into exactly one of these categories:
- materials_access
- schedule
- assignment
- upcoming_exams
- instructors_contact
- information
- admin_add (if a class rep adds data)

Rules:
- Return ONLY valid JSON.
- If unclear, return intent="unknown" and other fields null.

JSON SCHEMA:
{
  "role": "student | admin",
  "intent": "<topic | admin_add | unknown>",
  "topic": "<materials_access | schedule | assignment | upcoming_exams | instructors_contact | information | null>",
  "action": "<read | add | update | null>",
  "summary": "<short plain-English summary>"
}
"""

def classify_message(user_message: str):
    try:
        # 2. We pass examples in the user context to help the model learn the pattern
        user_content = f"""
Here are examples of how to classify:

Message: "Any assignments due this week?"
Output: {{"role": "student", "intent": "assignment", "topic": "assignment", "action": "read", "summary": "asking about upcoming assignment deadlines"}}

Message: "How do I contact our physics instructor?"
Output: {{"role": "student", "intent": "instructors_contact", "topic": "instructors_contact", "action": "read", "summary": "requesting instructor contact details"}}

Message: "Add math exam on Feb 25 at 10 AM"
Output: {{"role": "admin", "intent": "admin_add", "topic": "upcoming_exams", "action": "add", "summary": "adding a new math exam with date and time"}}

Now classify this message:
"{user_message}"
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": user_content}
            ],
            temperature=0,
            # 3. CRITICAL FIX: Force the model to output valid JSON
            response_format={"type": "json_object"}
        )

        # ai_output = response.choices[0].message.content.strip()

        # # 4. Parse the clean JSON
        # return json.loads(ai_output)
        ai_output = response.choices[0].message.content.strip()

        # remove markdown if present
        if ai_output.startswith("```"):
            ai_output = ai_output.split("```")[1]

        return json.loads(ai_output)

    

    except Exception as e:
        print(f"CLASSIFIER ERROR: {e}")
        # Return a safe fallback so the bot doesn't crash
        return {
            "role": "student",
            "intent": "unknown",
            "topic": None,
            "action": None,
            "summary": "Error processing message"
        }

# --- TEST ---
if __name__ == "__main__":
    test_msg = "Any assignments due this week?"
    result = classify_message(test_msg)
    print(json.dumps(result, indent=2))
