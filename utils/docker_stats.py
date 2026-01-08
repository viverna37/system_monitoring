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
    result = []

    for c in containers:
        s = c.stats(stream=False)

        cpu_percent = 0.0

        try:
            cpu_delta = (
                s["cpu_stats"]["cpu_usage"]["total_usage"]
                - s["precpu_stats"]["cpu_usage"]["total_usage"]
            )
            system_delta = (
                s["cpu_stats"]["system_cpu_usage"]
                - s["precpu_stats"]["system_cpu_usage"]
            )

            online_cpus = s["cpu_stats"].get("online_cpus")

            if online_cpus is None:
                online_cpus = len(
                    s["cpu_stats"]["cpu_usage"].get("percpu_usage", [])
                )

            if system_delta > 0 and online_cpus > 0:
                cpu_percent = (cpu_delta / system_delta) * online_cpus * 100.0
        except Exception:
            cpu_percent = 0.0

        mem_stats = s.get("memory_stats", {})
        mem_usage = mem_stats.get("usage", 0)
        mem_limit = mem_stats.get("limit", 0)

        net = s.get("networks", {})
        rx = sum(v.get("rx_bytes", 0) for v in net.values())
        tx = sum(v.get("tx_bytes", 0) for v in net.values())

        result.append({
            "name": c.name,
            "cpu": round(cpu_percent, 2),
            "mem_used": mem_usage,
            "mem_limit": mem_limit,
            "net_rx": rx,
            "net_tx": tx,
        })

    return result
