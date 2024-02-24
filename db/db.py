# import os
# from dotenv import load_dotenv
# import psycopg2


# load_dotenv()


# db_config = {
#     'dbname': os.getenv("DB_NAME"),
#     'user': os.getenv("DB_USER"),
#     'password': os.getenv("DB_PASSWORD"),
#     'host': os.getenv("DB_HOST"),
#     'port': os.getenv("DB_PORT"),
#     'sslmode': 'disable'
# }


# def get_connection():
#     return psycopg2.connect(**db_config)


# def add_notification(chat_id, message, notify_time):
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute('''
#         INSERT INTO notifications (chat_id, message, notify_time)
#         VALUES (?, ?, ?)
#     ''', (chat_id, message, notify_time))

#     connection.commit()
#     connection.close()


# def get_notifications():
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute('''
#         SELECT id, chat_id, message FROM notifications
#         WHERE notify_time <= datetime('now')
#     ''')

#     notifications = cursor.fetchall()
#     connection.close()
#     return notifications


# def delete_notification(notification_id):
#     connection = get_connection()
#     cursor = connection.cursor()

#     cursor.execute('''
#         DELETE FROM notifications WHERE id = ?
#     ''', (notification_id,))

#     connection.commit()
#     connection.close()

