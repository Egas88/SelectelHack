# from apscheduler.schedulers.background import BackgroundScheduler
# from bot import bot
# import datetime
# from db.db import get_notifications, delete_notification, add_notification

# scheduler = BackgroundScheduler()
# scheduler.start()

# def add_notification_on_donation_plan(chat_id, selected_date, message_text):
#     notify_time = datetime.strptime(selected_date + " 08:00", "%Y-%m-%d %H:%M")
#     add_notification(chat_id, message_text, notify_time)


# def check_and_send_notifications():
#     notifications = get_notifications()
#     for notification_id, chat_id, message in notifications:
#         bot.send_message(chat_id, message)
#         delete_notification(notification_id)


# scheduler.add_job(check_and_send_notifications, 'interval', minutes=1)