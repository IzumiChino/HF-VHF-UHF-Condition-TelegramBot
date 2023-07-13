import requests
import random
import time
import re
import os
from datetime import datetime, time, timedelta
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import utc

TOKEN = 'INPUT_YOUR_TOKEN_HERE'
URL = 'INPUT_YOUR_URL_HERE'
FREQUENCY_TABLE_URL = 'http://www.eibispace.de/dx/freq-a23.txt'
CACHE_FILE_PATH = 'frequency_table.txt'  # 缓存文件路径
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
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot commands:\n/getcondition To get the image of condition\n/help To list commands of the bot\n/zako To simulate Mesugakis(メスガキ/雌小鬼)\n/frequency 列出在频率上的所有广播(频率表来源于Eibi)\nAuthor:Mashiro Chino\nGithub:https://github.com/IzumiChino/HF-VHF-UHF-Condition-TelegramBot")

def zako_random():
    sentences = [ "杂鱼お兄ちゃん，你就是个软蛋呢~♡", "呐呐~杂鱼哥哥，你真是个快软了的家伙呢~♡", "真是杂鱼呢~♡", "呐呐~杂鱼哥哥不会这样就被捉弄的不会说话了吧♡真是弱哎♡~", "嘻嘻~杂鱼哥哥不会以为竖个大拇哥就能欺负我了吧~不会吧♡不会吧♡杂鱼哥哥怎么可能欺负得了别人呢~只能欺负自己哦♡~", "哥哥真是好欺负啊♡嘻嘻~", "哎♡~杂鱼说话就是无趣唉~只会发一张表情包的笨蛋到处都有吧♡", "呐呐~杂鱼哥哥发这个是想教育我吗~嘻嘻~怎么可能啊♡", "什么嘛~废柴哥哥会想这种事情啊~唔呃，把你肮脏的目光拿开啦~很恶心哦♡", "哼...！这...这样已经够了♡，明明这种微不足道的小事，也要拐上雌小鬼嘛...", "雌小鬼一没有招惹大哥哥，二没有对大哥哥做坏坏的事情♡雌小鬼每天都费劲心思戏弄大哥哥，你这杂鱼只想着对我做涩涩的事情，我的期待就是被你这样的笨蛋破坏了~♡", "杂鱼~♡杂鱼~♡", "哥哥真是弱呢，这才几下就射了~♡杂鱼~♡", "哥哥真好捉弄呢~♡嘻嘻", "哥哥是想做涩涩的事情了吧~真是恶心呢~♡", "杂鱼哥哥的怎么这么小啊~♡根本没法满足我哦~♡", "杂鱼哥哥连填满我都做不到呢~♡", "哥哥因为没法填满我恼羞成怒了吗~♡嘻嘻~真是杂鱼呢~♡", "哈？！这种问题也要问？你这个杂鱼♡真是弱啊♡~好吧，说吧，我看看你能问出什么变态的问题来♡", "呐呐~杂鱼哥哥，你真是个毫无挑战的对手呢~♡", "嘻嘻~杂鱼哥哥，你的尝试真是可笑呢~♡", "哎♡~杂鱼哥哥，你真是个无聊的笨蛋啊~♡", "哥哥真是好好笑啊~嘻嘻~♡", "杂鱼哥哥，你就是个表情包发狂的笨蛋呢~♡", "呐呐~杂鱼哥哥，你想教育我吗？哈哈~不可能啦~♡", "什么嘛~废柴哥哥，你居然会想到那种恶心的事情~呕吐♡", "哼...！这...这样就够了吧♡，你这种微不足道的小人物，还真是自以为是呢...", "我从来没有招惹大哥哥，更没有对大哥哥做出伤害的行为哦~每天都费心思戏弄大哥哥，可你这个杂鱼只会想着对我做下流的事情，真是毁了我的期待呢~♡", "杂鱼~♡杂鱼~♡你就是个渣男呢~♡", "哥哥真是容易满足了，这么快就射了~♡杂鱼~♡", "哥哥真擅长捉弄我呢~♡嘻嘻~", "哥哥是不是心里想着下流的事情呀~真是恶心呢~♡", "杂鱼哥哥的大小让人失望啊~♡根本无法满足我哦~♡", "哥哥连填满我都做不到呢~♡真是个废物呢~♡", "哈？！连这种问题都要问？你这个杂鱼♡真是太无能了♡~好吧，问吧，看看你能问出什么低俗的问题来♡", "杂鱼哥哥，你真是个幼稚的小孩呢~♡", "呐呐~杂鱼哥哥，你的自以为是真是可笑呢~♡", "嘻嘻~杂鱼哥哥，你就只会嘴上说说而已呢~♡", "杂鱼哥哥，你就是个无趣透顶的笨蛋呢~♡", "呐呐~杂鱼哥哥，你的言行让人感到厌恶呢~♡", "什么嘛~废柴哥哥，你居然会想这种事情~呃，太恶心了♡", "哼...！这...这样已经够了吗♡，明明这种微不足道的小事，也要拐上雌小鬼嘛...", "雌小鬼一没有招惹大哥哥，二没有对大哥哥做坏坏的事情♡雌小鬼每天都费劲心思戏弄大哥哥，你这杂鱼只想着对我做涩涩的事情，真是破坏了我的期待呢~♡", "哈？！这种问题也要问？你这个杂鱼♡真是弱啊♡~好吧，说吧，我看看你能问出什么变态的问题来♡"]
    return random.choice(sentences)

def zako(update, context):
    zakotimes = 10
    sent = set()
    while zakotimes:
        sentence = zako_random()
        if sentence not in sent:
            sent.add(sentence)
            context.bot.send_message(chat_id=update.effective_chat.id, text=sentence)
            zakotimes -= 1
    photo_url = "https://imgse.com/i/pChAKWF"
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_url)


def download_frequency_table():
    try:
        response = requests.get(FREQUENCY_TABLE_URL)
        if response.status_code == 200:
            return response.text
        else:
            print("下载频率表失败。HTTP状态码:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("下载频率表失败：", e)
        return None


def search_broadcast_stations(frequency, frequency_table):
    matches = re.findall(r'(\d+(\.\d+)?)\s+(.+)', frequency_table)
    stations = []
    for match in matches:
        freq, _, station = match
        if float(freq) == frequency:
            stations.append(station.strip())
    return stations

def search_station(update, context):
    chat_id = update.effective_chat.id
    try:
        frequency = float(context.args[0])
    except (IndexError, ValueError):
        context.bot.send_message(chat_id=chat_id, text="无效的频率。请提供有效的频率（单位：千赫兹）。")
        return

    frequency_table = download_frequency_table()
    if frequency_table:
        stations = search_broadcast_stations(frequency, frequency_table)
        if stations:
            response = f"找到频率为 {frequency} 千赫兹的广播电台（时间均为UTC时间）：\n"
            response += '\n'.join(stations)
            context.bot.send_message(chat_id=chat_id, text=response)
        else:
            context.bot.send_message(chat_id=chat_id, text=f"未找到频率为 {frequency} 千赫兹的广播电台。")
    else:
        context.bot.send_message(chat_id=chat_id, text="下载频率表失败，请稍后重试。")


def main():
    fetch_image_data()  # 预先获取并缓存图片数据

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    get_condition_handler = CommandHandler('getcondition', send_image_to_user)
    help_handler = CommandHandler('help', helpcommand)
    zako_handler = CommandHandler('zako', zako)
    search_staion_handler = CommandHandler('frequency', search_station)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(get_condition_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(zako_handler)
    dispatcher.add_handler(search_staion_handler)

    scheduler.add_job(fetch_image_data, 'cron', hour=0, minute=0, second=0)  # 每天UTC时间00:00运行任务
    scheduler.start()

    updater.start_polling()

if __name__ == '__main__':
    main()
