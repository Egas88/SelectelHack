# from db.db import get_connection


# def create_notifications_table():
#     connection = get_connection()
#     cursor = connection.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS notifications (
#             id SERIAL PRIMARY KEY,
#             chat_id INTEGER NOT NULL,
#             message TEXT NOT NULL,
#             notify_time DATETIME NOT NULL
#         )
#     ''')
#     connection.commit()
#     connection.close()