from app import Application
from bot import Messenger

if __name__ == "__main__":
  app = Application()
  myBot = Messenger(start_scraper=app.run)
  myBot.polling()
