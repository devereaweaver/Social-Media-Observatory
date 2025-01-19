# Connect to the PostgreSQL database server
from config import config
import sqlalchemy as sa

engine = sa.create_engine(
    f"postgresql://"
    f"{config['telegram-db']['user']}:"
    f"{config['telegram-db']['password']}:"
    f"@{config['telegram-db']['host']}:"
    f"{config['telegram-db']['port']}/"
    f"{config['telegram-db']['dbname']}",
    echo=True,
)