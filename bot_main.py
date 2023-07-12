import requests
import random
from datetime import datetime, time, timedelta
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

TOKEN = '6043397370:AAFc2MUqXP_rKgYCcAMG6mXLcpLYl77Akmc'
URL = 'https://www.hamqsl.com/solar101vhfpic.php'
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
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot commands:\n/getcondition To get the image of condition\n/help To list commands of the bot\n/zako To simulate Mesugakis(メスガキ/雌小鬼)\nAuthor:Mashiro Chino\nGithub:https://github.com/IzumiChino/HF-VHF-UHF-Condition-TelegramBot")

def zako_random():
    sentences = ["杂鱼~♡", "杂鱼お兄ちゃん，这么快就软了呢~♡", "真是杂鱼呢~♡", "呐呐~杂鱼哥哥不会这样就被捉弄的不会说话了吧♡真是弱哎♡~", "嘻嘻~杂鱼哥哥不会以为竖个大拇哥就能欺负我了吧~不会吧♡不会吧♡杂鱼哥哥怎么可能欺负得了别人呢~只能欺负自己哦♡~", "哥哥真是好欺负啊♡嘻嘻~", "哎♡~杂鱼说话就是无趣唉~只会发一张表情包的笨蛋到处都有吧♡", "呐呐~杂鱼哥哥发这个是想教育我吗~嘻嘻~怎么可能啊♡", "什么嘛~废柴哥哥会想这种事情啊~唔呃，把你肮脏的目光拿开啦~很恶心哦♡", "哼...！这...这样已经够了♡，明明这种微不足道的小事，也要拐上雌小鬼嘛...", "雌小鬼一没有招惹大哥哥，二没有对大哥哥做坏坏的事情♡雌小鬼每天都费劲心思戏弄大哥哥，你这杂鱼只想着对我做涩涩的事情，我的期待就是被你这样的笨蛋破坏了~♡", "杂鱼~♡杂鱼~♡", "哥哥真是弱呢，这才几下就射了~♡杂鱼~♡", "哥哥真好捉弄呢~♡嘻嘻", "哥哥是想做涩涩的事情了吧~真是恶心呢~♡", "杂鱼哥哥的怎么这么小啊~♡根本没法满足我哦~♡", "杂鱼哥哥连填满我都做不到呢~♡", "哥哥因为没法填满我恼羞成怒了吗~♡嘻嘻~真是杂鱼呢~♡"]
    return random.choice(sentences)


def zako(update, context):
    zakotimes = 10
    while zakotimes:
        context.bot.send_message(chat_id=update.effective_chat.id, text=zako_random())
        zakotimes = zakotimes - 1

def main():
    fetch_image_data()  # 预先获取并缓存图片数据

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    get_condition_handler = CommandHandler('getcondition', send_image_to_user)
    help_handler = CommandHandler('help', helpcommand)
    zako_handler = CommandHandler('zako', zako)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(get_condition_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(zako_handler)

    scheduler.add_job(fetch_image_data, 'cron', hour=0, minute=0, second=0)  # 每天UTC时间00:00运行任务
    scheduler.start()

    updater.start_polling()

if __name__ == '__main__':
    main()
