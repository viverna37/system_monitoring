import os

import docker
import subprocess

import dotenv

from config import load_config

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


def exec_sql_in_container(
        container_name: str,
        db_name: str,
        user: str,
        sql: str
) -> str:
    """
    Выполняет SQL-запрос внутри docker-контейнера с PostgreSQL
    и возвращает stdout.
    """

    cmd = [
        "docker", "exec", "-i",
        container_name,
        "psql",
        "-U", user,
        "-d", db_name,
        "-c", sql,
    ]

    env = None
    config = load_config()
    password = config.server.pgpassword
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"SQL error:\n{result.stderr.strip()}"
        )

    return result.stdout.strip()


def create_schemas(
        schemas_name: str,
        schemas_user: str
) -> bool:
    """
    Создает схему в main_db + пользователя, автоматически ограничивая права
    """

    sql = {
        "create": f"CREATE SCHEMA {schemas_name};",
        "create_user": f"CREATE USER {schemas_user} WITH PASSWORD 'super-strong-password';",
        "limit_all_users": f"GRANT USAGE, CREATE ON SCHEMA {schemas_name} TO {schemas_user};",
        "limit_new_user": f"ALTER ROLE {schemas_user} SET search_path TO {schemas_name};",
        "rewoke_public": f"REVOKE ALL ON SCHEMA public FROM {schemas_user};"
    }

    config = load_config()

    for key, value in sql:
        cmd = [
            "docker", "exec", "-i",
            "postgres",
            "psql",
            "-U", "admin",
            "-d", 'main_db',
            "-c", value,
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            env={"PATH": os.environ["PATH"],
                 "PGPASSWORD": config.server.pgpassword, },
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"SQL error:\n{result.stderr.strip()}"
            )

    return True
