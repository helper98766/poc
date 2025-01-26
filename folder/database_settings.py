import os

# Configuration for SQLite
GLOBAL_SETTINGS = {
    "sqlite_filename": os.getenv("SQLITE_FILENAME", "example.db"),  # SQLite database name
    "echo_sql": bool(os.getenv("ECHO_SQL", False)),
}

def get_sqlite_filename():
    """
    Returns the SQLite database filename.
    """
    return GLOBAL_SETTINGS["sqlite_filename"]

def get_echo_sql():
    """
    Returns whether SQL echo mode is enabled.
    """
    return GLOBAL_SETTINGS["echo_sql"]