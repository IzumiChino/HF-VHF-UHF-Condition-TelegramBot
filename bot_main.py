import requests
from datetime import datetime, time, timedelta
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

TOKEN = 'INPUT_YOUR_TOKEN_HERE'
URL = 'INPUT_YOUR_URL_HERE'
SEND_TIME = time(hour=0, minute=0, second=0)

bot = Bot(token=TOKEN)
scheduler = BackgroundScheduler(timezone=utc)

# 缓存的图片数据和最后更新时间
cached_image_data = None
last_update_time = None

def get_image_url():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.content
    return None

def fetch_image_data():
    global cached_image_data, last_update_time
    cached_image_data = get_image_url()
    last_update_time = datetime.utcnow()

def send_image_to_user(update, context):
    if cached_image_data:
        chat_id = update.effective_chat.id
        bot.send_photo(chat_id=chat_id, photo=cached_image_data, filename='image.jpg')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to get the image.")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="请通过 /getcondition 指令来获取当日传播预测图")

def helpcommand(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot commands:\n/getcondition To get the image of condition\n/help To list commands of the bot\nAuthor:Mashiro Chino")

def main():
    fetch_image_data()  # 预先获取并缓存图片数据

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    get_condition_handler = CommandHandler('getcondition', send_image_to_user)
    help_handler = CommandHandler('help', helpcommand)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(get_condition_handler)
    dispatcher.add_handler(help_handler)

    scheduler.add_job(fetch_image_data, 'cron', hour=0, minute=0, second=0)  # 每天UTC时间00:00运行任务
    scheduler.start()

    updater.start_polling()

if __name__ == '__main__':
    main()
