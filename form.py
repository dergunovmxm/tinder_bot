from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

import settings
from emoji import emojize
from utils import *


def form_start(update, contex):
    smile = emojize(settings.EMOJI[0], use_aliases=True)
    update.message.reply_text(f"Начнём регистрацию{smile}! Для начала скажите вашу фамилию и имя", reply_markup=None)
    return "name"


def form_name(update, contex):
    user_name = update.message.text.split()
    if user_name[0] == "/stop":
        contex.user_data.clear()
        return ConversationHandler.END
    elif len(user_name) != 2:
        update.message.reply_text("Пожалуйста, введите фамилию и имя", reply_markup=None)
        return "name"
    else:
        contex.user_data["form"] = {"name": user_name}
        update.message.reply_text(f"Укажите вашу ссылку на телеграм или вк", reply_markup=None)
        return "call"


def form_call(update, contex):
    user_call = update.message.text.split()
    if user_call == "/stop":
        contex.user_data.clear()
        return ConversationHandler.END
    else:
        contex.user_data["form"] = {"call": user_call}
        smile = emojize(settings.EMOJI[3], use_aliases=True)
        update.message.reply_text(f"Оцените знания по предметам{smile}", reply_markup=subjects_keyboard())
        return "how_know"


def form_subjects_know(update, contex):
    user_subject = update.message.text

    if user_subject == "/stop":
        contex.user_data.clear()
        return ConversationHandler.END
    else:
        contex.user_data["form"] = {"bad_know": user_subject}
        smile = emojize(settings.EMOJI[3], use_aliases=True)
        update.message.reply_text(f"Выберите предмет для  оценки{smile}",
                                  reply_markup=subjects_keyboard())
        return "how_know"


def form_how_know(update, contex):
    user_message = update.message.text
    if user_message == "/stop":
        contex.user_data.clear()
        return ConversationHandler.END
    elif user_message == "Далее":
        form_that_all(update, contex)
        return
    else:
        update.message.reply_text("Оцените ваш уровень знаний по предмету от 1 до 10, "
                                  "где чем меньше число, тем хуже знаешь предмет", reply_markup=how_know_keyboard())
        return "subjects_know"


def form_that_all(update, contex):
    smile = emojize(settings.EMOJI[4], use_aliases=True)
    update.message.reply_text(f"Отлично!{smile} Теперь мы можем подобрать вам друга для учёбы. Найти?",
                              reply_markup=yes_no_keyboard())
