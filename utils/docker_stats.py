import docker

client = docker.from_env()

def bytes_to_mb(b: int) -> float:
    return b / 1024 / 1024


def format_mem(used, limit):
    if limit == 0:
        return f"{bytes_to_mb(used):.1f} MB"
    return f"{bytes_to_mb(used):.1f} / {bytes_to_mb(limit):.1f} MB"

def get_docker_stats():
    containers = client.containers.list()
    stats = []

    for c in containers:
        s = c.stats(stream=False)

        cpu_delta = (
            s["cpu_stats"]["cpu_usage"]["total_usage"]
            - s["precpu_stats"]["cpu_usage"]["total_usage"]
        )
        system_delta = (
            s["cpu_stats"]["system_cpu_usage"]
            - s["precpu_stats"]["system_cpu_usage"]
        )

        cpu_percent = 0.0
        if system_delta > 0:
            cpu_percent = (
                cpu_delta / system_delta
            ) * len(s["cpu_stats"]["cpu_usage"]["percpu_usage"]) * 100.0

        mem_usage = s["memory_stats"]["usage"]
        mem_limit = s["memory_stats"].get("limit", 0)

        net = s.get("networks", {})
        rx = sum(v["rx_bytes"] for v in net.values())
        tx = sum(v["tx_bytes"] for v in net.values())

        stats.append({
            "name": c.name,
            "cpu": round(cpu_percent, 2),
            "mem_used": mem_usage,
            "mem_limit": mem_limit,
            "net_rx": rx,
            "net_tx": tx,
        })

    return stats
