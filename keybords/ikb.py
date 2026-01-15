from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class LogsCb(CallbackData, prefix="logs"):
    name: str
    page: int


class IKB:
    class Back:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()
            kb.add(
                InlineKeyboardButton(text="⬅️ Назад", callback_data="exit")
            )
            kb.adjust(1)
            return kb.as_markup()

    class Menu:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()

            kb.add(InlineKeyboardButton(text="🖥 Мониторинг сервера", callback_data="system_monitoring"))
            kb.add(InlineKeyboardButton(text="⚙️ Server menu", callback_data="server_menu"))
            kb.add(InlineKeyboardButton(text="🐳 Docker menu", callback_data="docker_menu"))

            kb.adjust(1)
            return kb.as_markup()

    class Server:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()

            kb.add(InlineKeyboardButton(text="🔄 Перезапуск", callback_data="server_menu"))
            kb.add(InlineKeyboardButton(text="⛔ Выключение", callback_data="server_menu"))
            kb.add(InlineKeyboardButton(text="🧪 Тест", callback_data="213"))
            kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="exit"))

            kb.adjust(1)
            return kb.as_markup()

    class Docker:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()

            kb.add(InlineKeyboardButton(text="📊 Мониторинг Docker", callback_data="docker_monitoring"))
            kb.add(InlineKeyboardButton(text="📈 Статистика Docker", callback_data="docker_stats"))
            kb.add(InlineKeyboardButton(text="🛠 Управление", callback_data="docker_management"))
            kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="exit"))

            kb.adjust(1)
            return kb.as_markup()

    class DockerManagement:
        @staticmethod
        def get_menu() -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()

            kb.add(InlineKeyboardButton(text="🧩 Создать схему", callback_data="create_schemas"))
            kb.add(InlineKeyboardButton(text="📦 Контейнеры", callback_data="containers"))
            kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="exit_2"))

            kb.adjust(1)
            return kb.as_markup()

        @staticmethod
        def get_management_menu(name: str) -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()

            kb.add(InlineKeyboardButton(text="🔄 Перезагрузить", callback_data=f"reboot:{name}"))
            kb.add(InlineKeyboardButton(text="📄 Логи", callback_data=f"logs:{name}"))
            kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="exit_2"))

            kb.adjust(1)
            return kb.as_markup()

        @staticmethod
        def get_containers_keyboard(containers: list) -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()

            for c in containers:
                kb.add(
                    InlineKeyboardButton(
                        text=f"📦 {c['name']}",
                        callback_data=f"card:{c['name']}"
                    )
                )

            kb.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_2"))
            kb.adjust(1)
            return kb.as_markup()

        @staticmethod
        def logs_pagination_kb(
            name: str,
            page: int,
            total: int,
        ) -> InlineKeyboardMarkup:
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
                    text=f"📄 {page + 1}/{total}",
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
