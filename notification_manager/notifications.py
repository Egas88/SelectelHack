# from apscheduler.schedulers.background import BackgroundScheduler
# from bot import bot
# import datetime
# from db.db import get_nearest_notification, delete_notification, add_notification

# scheduler = BackgroundScheduler()
# scheduler.start()

# def add_notification_on_donation_plan(chat_id, selected_date, message_text):
#     notify_time = datetime.strptime(selected_date + " 07:00", "%Y-%m-%d %H:%M")
#     add_notification(chat_id, message_text, notify_time)
#     check_notifications()


# def check_notifications():
#     notification = get_nearest_notification()
#     scheduler.add_job(bot.send_message, 'date', run_date = notification[3], args=[int(notification[1]), notification[2]])
#     delete_notification(notification[0])

