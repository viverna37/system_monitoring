from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class IKB:
    class Menu:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:
            keyboard = InlineKeyboardBuilder()

            keyboard.add(InlineKeyboardButton(text="Мониторинг Server", callback_data="system_monitoring"))
            keyboard.add(InlineKeyboardButton(text="Server menu", callback_data="server_menu"))
            keyboard.add(InlineKeyboardButton(text="Docker menu", callback_data="docker_menu"))

            keyboard.adjust(1)

            return keyboard.as_markup()

    class Server:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:
            keyboard = InlineKeyboardBuilder()

            keyboard.add(InlineKeyboardButton(text="Создаить схему", callback_data="server_menu"))
            keyboard.add(InlineKeyboardButton(text="Перезапуск", callback_data="server_menu"))
            keyboard.add(InlineKeyboardButton(text="Выключение", callback_data="server_menu"))
            keyboard.add(InlineKeyboardButton(text="123", callback_data="213"))
            keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit"))
            keyboard.adjust(1)

            return keyboard.as_markup()

    class Docker:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:

            keyboard = InlineKeyboardBuilder()

            keyboard.add(InlineKeyboardButton(text="Мониторинг Docker", callback_data="docker_monitoring"))
            keyboard.add(InlineKeyboardButton(text="Статистика Docker", callback_data="docker_stats"))
            keyboard.add(InlineKeyboardButton(text="Управление", callback_data="docker_management"))
            keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit"))
            keyboard.adjust(1)


            return keyboard.as_markup()

    class DockerManagement:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:

            keyboard = InlineKeyboardBuilder()

            keyboard.add(InlineKeyboardButton(text="Создать схему", callback_data="create_schemas"))
            keyboard.add(InlineKeyboardButton(text="Контейнеры", callback_data="containers"))
            keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit_2"))

            keyboard.adjust(1)

            return keyboard.as_markup()

        @staticmethod
        def get_management_menu(id) -> InlineKeyboardMarkup:

            keyboard = InlineKeyboardBuilder()

            keyboard.add(InlineKeyboardButton(text="Перезагрузить", callback_data=f"reboot_{id}"))
            keyboard.add(InlineKeyboardButton(text="Логи", callback_data="logs_{id}"))
            keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit_2"))

            keyboard.adjust(1)

            return keyboard.as_markup()