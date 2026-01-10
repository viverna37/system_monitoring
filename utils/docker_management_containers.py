import logging
from datetime import datetime, timezone
from typing import Any

import docker

client = docker.from_env()


def format_timedelta(td) -> str:
    if not td:
        return "-"
    seconds = int(td.total_seconds())
    h, rem = divmod(seconds, 3600)
    m, _ = divmod(rem, 60)
    return f"{h}h {m}m"

def get_containers()-> list[dict[str, Any]]:
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
            "uptime": uptime,
            "id": c.id
        })

    return result
from datetime import datetime, timezone
from typing import Optional


def get_container_by_name(name: str) -> Optional[dict]:
    print(name)
    logging.Logger(name, level=logging.WARNING)
    for c in client.containers.list(all=True):
        if c.name != name:
            continue

        started_at = c.attrs["State"].get("StartedAt")
        uptime = None

        if c.status == "running" and started_at:
            start_time = datetime.fromisoformat(
                started_at.replace("Z", "+00:00")
            )
            uptime = datetime.now(timezone.utc) - start_time

        return {
            "name": c.name,
            "status": c.status,
            "image": c.image.tags[0] if c.image.tags else "unknown",
            "uptime": uptime,
            "id": c.id,
        }

    return None
