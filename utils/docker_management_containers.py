import logging
from datetime import datetime, timezone
from typing import Any, List

import docker

client = docker.from_env()


def split_text(text: str, limit: int = 1024) -> list[str]:
    return [text[i:i + limit] for i in range(0, len(text), limit)]


def format_timedelta(td) -> str:
    if not td:
        return "-"
    seconds = int(td.total_seconds())
    h, rem = divmod(seconds, 3600)
    m, _ = divmod(rem, 60)
    return f"{h}h {m}m"


def get_containers() -> list[dict[str, Any]]:
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


def reboot_container(name: str) -> bool:
    """
    Перезапускает контейнер по имени
    """
    try:
        container = client.containers.get(name)
        container.restart()
        return True
    except docker.errors.NotFound:
        return False
    except Exception as e:
        raise RuntimeError(f"Failed to restart container: {e}")


def get_container_logs(
        name: str,
        tail: int = 100,
        limit: int = 1024,
) -> List[str]:
    """
    Возвращает логи контейнера, разбитые на части <= limit
    """
    try:
        container = client.containers.get(name)

        raw_logs = container.logs(
            tail=tail,
            stdout=True,
            stderr=True,
            timestamps=False,
        )

        text = raw_logs.decode(errors="ignore").strip()
        if not text:
            return ["(logs are empty)"]

        return split_text(text, limit)

    except docker.errors.NotFound:
        return ["Container not found"]
    except Exception as e:
        return [f"Error reading logs: {e}"]
