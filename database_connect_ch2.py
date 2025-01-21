# Connect to the PostgreSQL database server
from config import config
import sqlalchemy as sa

try:
    engine = sa.create_engine(
        f"postgresql://"
        f"{config['telegram-db']['user']}:"
        f"{config['telegram-db']['password']}:"
        f"@{config['telegram-db']['host']}:"
        f"{config['telegram-db']['port']}/"
        f"{config['telegram-db']['dbname']}",
        echo=True,
    )

    connection = engine.connect()
    print("Connection to PostgreSQL DB successful")

except Exception as e:
    print("Connection to PostgreSQL DB failed")
