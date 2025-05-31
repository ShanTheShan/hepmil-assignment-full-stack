from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from pypdf import PdfReader


class Messenger:
    def __init__(self, start_scraper):
        load_dotenv()
        myKey = os.getenv('key')
        self.start_scraper = start_scraper

        self.app = ApplicationBuilder().token(myKey).build()

        self.app.add_handler(CommandHandler("start", self.greet_command))
        self.app.add_handler(CommandHandler("begin", self.begin_command))
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_response))

    async def greet_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            'Hello, I am the bot for the hepmil_assignment for full stack engineer. I scrape r/memes for the top 20 posts in the past 24 hours and return a report. Type /begin to start.'
        )

    async def begin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        await update.message.reply_text('Scraping and generating report, please wait...')
        self.start_scraper()

        #send pdf
        document = open('memes_report.pdf','rb')
        await context.bot.send_document(chat_id,document)

    async def handle_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Hey, I only serve one purpose! Run /start to see what I do.")

    def polling(self):
        print("Listening...")
        self.app.run_polling()
