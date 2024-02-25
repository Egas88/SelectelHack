users_dict = {}
is_possible_input = True
additional_input = True

is_reg = False
is_login = False
is_change_pass = False
is_change_phone = False
is_change_email = False
is_aricles = False
old_man_pic_delete_message = 0

def get_username(chat_id):
    if chat_id in users_dict:
        if "phone" in users_dict[chat_id]:
            return users_dict[chat_id]["phone"]
        elif "email" in users_dict[chat_id]:
            return users_dict[chat_id]["email"]
    return None


def get_password(chat_id):
    return users_dict[chat_id]["password"]
