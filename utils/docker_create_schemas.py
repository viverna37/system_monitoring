import docker
from config import load_config

client = docker.from_env()


def create_schemas(
    schemas_name: str,
) -> bool:
    """
    Создаёт схему и пользователя в PostgreSQL через Docker API
    """

    sql_commands = [
        f"CREATE SCHEMA {schemas_name};",
        f"CREATE USER {schemas_name + "_user"} WITH PASSWORD 'super-strong-password';",
        f"GRANT USAGE, CREATE ON SCHEMA {schemas_name} TO {schemas_name + "_user"};",
        f"ALTER ROLE {schemas_name + "_user"} SET search_path TO {schemas_name};",
        f"REVOKE ALL ON SCHEMA public FROM {schemas_name + "_user"};",
    ]

    config = load_config()

    container = client.containers.get("postgres")

    for sql in sql_commands:
        cmd = (
            f'psql -U admin -d main_db '
            f'-c "{sql}"'
        )

        exit_code, output = container.exec_run(
            cmd,
            environment={
                "PGPASSWORD": config.server.pgpassword
            }
        )

        if exit_code != 0:
            raise RuntimeError(
                f"SQL error:\n{output.decode()}"
            )

    return True
