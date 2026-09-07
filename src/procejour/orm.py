TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://data/db.sqlite3",
    },
    "apps": {
        "models": {
            "models": ["procejour.models"],
            "default_connection": "default",
            "migrations": "procejour.migrations",
        },
    },
}
