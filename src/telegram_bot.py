from os import getenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, ContextTypes
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv

load_dotenv()

groq_key = getenv('GROQ_KEY')
bot_token = getenv('INVENTORY_STEWARD_BOT_TOKEN')
mistral = 'mixtral-8x7b-32768'

llm = ChatGroq(name='Steward', api_key=groq_key, model=mistral)

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    user_message = update.message.text
    llm_response = await llm.ainvoke(user_message)
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text= llm_response.content)

application = ApplicationBuilder().token(bot_token).build()

echo_handler = MessageHandler(
    filters.TEXT
    & (~filters.COMMAND)
    ,respond)

application.add_handler(echo_handler)

if __name__ == '__main__':
    print('BOT RUNNING')

    application.run_polling()