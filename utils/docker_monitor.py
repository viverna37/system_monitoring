import docker
from datetime import datetime, timezone

client = docker.from_env()

def format_timedelta(td):
    if not td:
        return "-"
    seconds = int(td.total_seconds())
    h, rem = divmod(seconds, 3600)
    m, _ = divmod(rem, 60)
    return f"{h}h {m}m"


def docker_available() -> bool:
    try:
        client.ping()
        return True
    except Exception:
        return False


def get_containers():
    containers = client.containers.list(all=True)
    result = []

    for c in containers:
        started_at = c.attrs["State"].get("StartedAt")
        uptime = None

        if c.status == "running" and started_at:
            start_time = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
            uptime = datetime.now(timezone.utc) - start_time

        result.append({
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "unknown",
            "uptime": uptime
        })

    return result
