from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class IKB:
    class Menu:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:
            keyboard = InlineKeyboardBuilder()

            keyboard.add(InlineKeyboardButton(text="Мониторинг сервера", callback_data="system_monitoring"))
            keyboard.add(InlineKeyboardButton(text="Мониторинг сервера", callback_data="docker_monitoring"))

            keyboard.adjust(1)

            return keyboard.as_markup()