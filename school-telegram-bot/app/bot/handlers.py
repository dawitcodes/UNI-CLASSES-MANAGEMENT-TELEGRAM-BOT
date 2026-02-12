# from telegram import Update
# from telegram.ext import ContextTypes
# from app.ai.classifier import classify_message
# import json

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     user_message = update.message.text

#     try:
#         result = classify_message(user_message)
#         await update.message.reply_text(f"✅ Classified JSON:\n\n{json.dumps(result, indent=2)}")
#     except Exception as e:
#         await update.message.reply_text("❌ Error processing message.")
#         print(e)
        
# from app.ai.classifier import classify_message
# from app.services.router import route

# async def handle_message(update, context):
#     text = update.message.text

#     classification = classify_message(text)
#     response = route(classification, text)

#     await update.message.reply_text(response)

# from app.ai.classifier import classify_message
# from app.services.router import route
# from app.utils.permissions import is_admin

# async def handle_message(update, context):
#     text = update.message.text
#     user_id = update.message.from_user.id

#     classification = classify_message(text)

#     # 🔐 FORCE ADMIN ROLE IF USER IS ADMIN
#     if is_admin(user_id):
#         classification["role"] = "admin"

#     response = route(classification, text)
#     await update.message.reply_text(response)

from telegram import Update
from telegram.ext import ContextTypes
from app.ai.classifier import classify_message
from app.services.router import route
from app.utils.permissions import is_admin

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    # Step 1: classify message using AI
    classification = classify_message(text)

    # Step 2: enforce admin role if user is in admin list
    if is_admin(user_id):
        classification["role"] = "admin"

    # Step 3: route the message to the correct service
    response = route(classification, text)

    # Step 4: send the reply back to Telegram
    await update.message.reply_text(response)
