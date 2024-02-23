users_dict = {}


def get_username(chat_id):
    if chat_id in users_dict:
        if "phone" in users_dict[chat_id]:
            return users_dict[chat_id]["phone"]
        elif "email" in users_dict[chat_id]:
            return users_dict[chat_id]["email"]
    return None


def get_password(chat_id):
    return users_dict[chat_id]["password"]
