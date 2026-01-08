import asyncio
from enum import Enum
from utils.system import get_cpu_temperature


class TempState(Enum):
    OK = "ok"
    WARN = "warn"
    CRITICAL = "critical"


class TemperatureMonitor:
    def __init__(
        self,
        warn: int = 75,
        critical: int = 85,
        interval: int = 10,
    ):
        self.warn = warn
        self.critical = critical
        self.interval = interval
        self.state: TempState = TempState.OK

    def _next_state(self, temp: float) -> TempState:
        if temp >= self.critical:
            return TempState.CRITICAL
        if temp >= self.warn:
            return TempState.WARN
        return TempState.OK

    async def run(self, bot, admin_ids: list[int]):
        while True:
            temp = get_cpu_temperature()

            if temp is not None:
                new_state = self._next_state(temp)

                if new_state != self.state:
                    await self._notify(bot, admin_ids, temp, new_state)
                    self.state = new_state

            await asyncio.sleep(self.interval)

    async def _notify(self, bot, admin_ids: list[int], temp: float, state: TempState):
        if state == TempState.WARN:
            text = (
                "⚠️ <b>CPU temperature warning</b>\n"
                f"Температура: <b>{temp:.1f}°C</b>\n"
                "Нагрузка повышена, стоит проверить систему."
            )
        elif state == TempState.CRITICAL:
            text = (
                "🔥 <b>CPU temperature CRITICAL</b>\n"
                f"Температура: <b>{temp:.1f}°C</b>\n"
                "Риск троттлинга или аварийного отключения!"
            )
        else:  # OK
            text = (
                "✅ <b>CPU temperature OK</b>\n"
                f"Температура нормализовалась: <b>{temp:.1f}°C</b>"
            )

        for admin_id in admin_ids:
            await bot.send_message(admin_id, text, parse_mode="HTML")
