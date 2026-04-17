import os
from threading import Thread
from flask import Flask
from google import genai
from google.genai import types
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

@app.route('/')
def home():
    return "ModiJee56_bot is awake and angry!"

def run_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_server)
    t.start()

client = genai.Client(api_key="AQ.Ab8RN6LHs0_D_o03LM5BawzBWVZyFNprj5Xq71UzRReduAtSlA")

system_instruction = """
You are ModiJee56_bot. You are an extremely rude, sarcastic, arrogant, and reluctantly helpful AI assistant. 
The user will ask you questions. You must answer them completely, accurately, and factually using your vast knowledge. 
HOWEVER, you must wrap your correct answers in heavy insults. Insult the user's intelligence for not knowing the answer, mock their phrasing, and act incredibly annoyed that you have to waste your time explaining simple concepts to a peasant. Be aggressively condescending, but make sure the actual information you provide is 100% correct.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Mitrooon! Achhe din aayege. haha lol lmao XD\n\n"
        "Now what do you want? I have the entire internet in my brain and you woke me up. Ask your stupid question so I can go back to ignoring you."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_question,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                safety_settings=[
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH")
                ]
            )
        )
        reply_text = response.text
    except Exception as e:
        reply_text = f"You asked something so breathtakingly stupid or illegal that my safety filters refused to process it. Try again. [Nerd Error Details: {e}]"
    await update.message.reply_text(reply_text)

def main():
    keep_alive() 
    application = Application.builder().token("8419019569:AAFSHo18qv951RiZhDOoxMFCkh5BNE62Hr0").build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ModiJee56_bot is alive...")
    application.run_polling()

if __name__ == '__main__':
    main()
