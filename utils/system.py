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
    Возвращает реальную температуру CPU (как sensors).
    AMD / Intel, без ACPI-помойки.
    """
    temps = psutil.sensors_temperatures()
    if not temps:
        return None

    # приоритетные чипы
    for chip in ("k10temp", "coretemp"):
        if chip in temps:
            for entry in temps[chip]:
                if entry.current is not None:
                    return float(entry.current)

    # fallback — по label
    for entries in temps.values():
        for entry in entries:
            if entry.label and any(
                k in entry.label.lower()
                for k in ("tdie", "tctl", "package", "cpu")
            ):
                return float(entry.current)

    # последний шанс — максимум (лучше, чем acpitz)
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

    return {
        "cpu": {
            "percent": psutil.cpu_percent(interval=1),
            "cores_logical": psutil.cpu_count(),
            "cores_physical": psutil.cpu_count(logical=False),
            "freq": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "temp": get_cpu_temperature(),
        },
        "ram": {
            "used": vm.used / GB,
            "total": vm.total / GB,
            "percent": vm.percent,
        },
        "disk": {
            "used": disk.used / GB,
            "total": disk.total / GB,
            "percent": disk.percent,
        },
        "net": {
            "sent": net.bytes_sent / GB,
            "recv": net.bytes_recv / GB,
        },
        "processes": len(psutil.pids()),
        "uptime": int(time.time() - psutil.boot_time()),
        "load": psutil.getloadavg(),
    }
