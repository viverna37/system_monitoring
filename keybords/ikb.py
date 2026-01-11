from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class LogsCb(CallbackData, prefix="logs"):
    name: str
    page: int

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
        def get_management_menu(name: str) -> InlineKeyboardMarkup:

            keyboard = InlineKeyboardBuilder()

            keyboard.add(InlineKeyboardButton(text="Перезагрузить", callback_data=f"reboot:{name}"))
            keyboard.add(InlineKeyboardButton(text="Логи", callback_data=f"logs:{name}"))
            keyboard.add(InlineKeyboardButton(text="Назад", callback_data="exit_2"))

            keyboard.adjust(1)

            return keyboard.as_markup()

        @staticmethod
        def get_containers_keyboard(containers: list) -> InlineKeyboardMarkup:
            keyboard = InlineKeyboardBuilder()

            for i in containers:
                keyboard.add(InlineKeyboardButton(text=i['image'], callback_data=f"card:{i['name']}"))

            keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_2"))

            keyboard.adjust(1)

            return keyboard.as_markup()
        @staticmethod
        def logs_pagination_kb(
                name: str,
                page: int,
                total: int,
        ):
            kb = InlineKeyboardBuilder()

            if page > 0:
                kb.add(
                    InlineKeyboardButton(
                        text="◀️",
                        callback_data=LogsCb(name=name, page=page - 1).pack()
                    )
                )

            kb.add(
                InlineKeyboardButton(
                    text=f"{page + 1}/{total}",
                    callback_data="noop"
                )
            )

            if page < total - 1:
                kb.add(
                    InlineKeyboardButton(
                        text="▶️",
                        callback_data=LogsCb(name=name, page=page + 1).pack()
                    )
                )

            kb.adjust(3)
            return kb.as_markup()