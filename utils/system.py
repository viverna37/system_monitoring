import psutil
import time
from typing import Optional


GB = 1024 ** 3


def format_uptime(seconds: int) -> str:
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)
    return f"{days}d {hours}h {minutes}m"


def get_cpu_temperature() -> Optional[float]:
    """
    Возвращает реальную температуру CPU (Tdie / Package),
    максимально близкую к выводу `sensors`.
    Работает для AMD и Intel.
    """
    temps = psutil.sensors_temperatures()
    if not temps:
        return None

    # Приоритетные чипы
    CHIP_PRIORITY = (
        "k10temp",     # AMD
        "coretemp",    # Intel
        "cpu_thermal",
    )

    # Приоритетные лейблы
    LABEL_PRIORITY = (
        "Tdie",
        "Tctl",
        "Package",
        "CPU",
    )

    # 1. Пробуем найти правильный чип
    for chip in CHIP_PRIORITY:
        if chip in temps:
            for entry in temps[chip]:
                if entry.current is not None:
                    return float(entry.current)

    # 2. Пробуем найти по label
    for entries in temps.values():
        for entry in entries:
            if entry.label:
                for label in LABEL_PRIORITY:
                    if label.lower() in entry.label.lower():
                        return float(entry.current)

    # 3. Фолбэк: берём максимальную температуру
    values = [
        entry.current
        for entries in temps.values()
        for entry in entries
        if entry.current is not None
    ]

    return float(max(values)) if values else None


def get_system_status() -> dict:
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()

    uptime_seconds = int(time.time() - psutil.boot_time())

    return {
        "cpu": {
            "percent": psutil.cpu_percent(interval=1),
            "cores_logical": psutil.cpu_count(),
            "cores_physical": psutil.cpu_count(logical=False),
            "freq_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "temp": get_cpu_temperature(),
        },
        "ram": {
            "used_gb": round(vm.used / GB, 2),
            "total_gb": round(vm.total / GB, 2),
            "percent": vm.percent,
        },
        "disk": {
            "used_gb": round(disk.used / GB, 2),
            "total_gb": round(disk.total / GB, 2),
            "percent": disk.percent,
        },
        "net": {
            "sent_gb": round(net.bytes_sent / GB, 3),
            "recv_gb": round(net.bytes_recv / GB, 3),
        },
        "processes": len(psutil.pids()),
        "uptime": format_uptime(uptime_seconds),
        "load": psutil.getloadavg(),
    }


if __name__ == "__main__":
    from pprint import pprint
    pprint(get_system_status())
