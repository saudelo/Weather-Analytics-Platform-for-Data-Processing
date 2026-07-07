import os
from dotenv import load_dotenv


load_dotenv()

def get_conn_string() -> str:
    return (
        f"host={os.getenv('DB_HOST')} "
        f"dbname={os.getenv('DB_NAME')} "
        f"user={os.getenv('DB_USER')} "
        f"password={os.getenv('DB_PASSWORD')} "
        f"port={os.getenv('DB_PORT')} "
        f"connect_timeout={os.getenv('DB_TIMEOUT')}"
    )