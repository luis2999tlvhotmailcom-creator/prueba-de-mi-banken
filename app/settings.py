import os

class Config:
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    dsn = os.getenv("DB_TNS_NAME")
    wallet_dir = os.getenv("DB_WALLET_DIR")
    wallet_password = os.getenv("DB_WALLET_PASSWORD")

    SQLALCHEMY_DATABASE_URI = (
        f"oracle+oracledb://{user}:{password}@{dsn}"
        f"?config_dir={wallet_dir}"
        f"&wallet_location={wallet_dir}"
        f"&wallet_password={wallet_password}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
