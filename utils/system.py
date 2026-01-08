import psutil
import time

def format_uptime(seconds: int) -> str:
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, _ = divmod(seconds, 60)
    return f"{days}d {hours}h {minutes}m"


GB = 1024 ** 3


def get_system_status() -> dict:
    vm = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()

    temps = psutil.sensors_temperatures()
    cpu_temp = None
    if temps:
        for name, entries in temps.items():
            if entries:
                cpu_temp = entries[0].current
                break

    uptime_seconds = int(time.time() - psutil.boot_time())

    return {
        "cpu": {
            "percent": psutil.cpu_percent(interval=1),
            "cores_logical": psutil.cpu_count(),
            "cores_physical": psutil.cpu_count(logical=False),
            "freq": psutil.cpu_freq().current if psutil.cpu_freq() else None,
            "temp": cpu_temp,
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
        "uptime": uptime_seconds,
        "load": psutil.getloadavg(),
    }
