from apscheduler.schedulers.background import BackgroundScheduler
from bot import bot
import datetime
from db.db import get_nearest_notification, delete_notification, add_notification

scheduler = BackgroundScheduler()
scheduler.start()

def add_notification_on_donation_plan(chat_id, selected_date, message_text):
    notify_time = datetime.datetime.strptime(selected_date, "%Y-%m-%d")
    add_notification(chat_id, message_text, notify_time)
    check_notifications()


def check_notifications():
    notification = get_nearest_notification()
    scheduler.add_job(send_notification, run_date = datetime.datetime(notification[3].year, notification[3].month, notification[3].day, 5, 0), args=[int(notification[1]), notification[2]])
    delete_notification(notification[0])


def send_notification(chat_id, message_text):
    bot.send_message(chat_id = chat_id, text=message_text)
