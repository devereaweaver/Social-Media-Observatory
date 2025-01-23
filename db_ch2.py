# db_ch2.py - database api

from config import config  # import the config manager object
import sqlalchemy as sa
from datetime import datetime

# Try to connect to database and create table
try:
    engine = sa.create_engine(
        f"postgresql://"
        f"{config['telegram-db']['user']}:"
        f"{config['telegram-db']['password']}"
        f"@{config['telegram-db']['host']}:"
        f"{config['telegram-db']['port']}/"
        f"{config['telegram-db']['dbname']}",
        echo=True,
    )

    # Create a metadata object to store table metadata
    meta = sa.MetaData()

    channel_metadata = sa.Table(
        'channel_metadata',
        meta, 
        sa.Column("channel_id", sa.types.BIGINT, primary_key=True),
        sa.Column("channel_name", sa.types.TEXT, unique=True),
        sa.Column("channel_title", sa.types.TEXT, default=None),
        sa.Column("channel_birthdate", sa.types.DateTime(timezone=True)),
        sa.Column("channel_bio", sa.types.TEXT, default=None),
        sa.Column("num_subscribers", sa.types.INTEGER, default=None),
        sa.Column("data_source", sa.types.TEXT, default="telegram-api"),
        sa.Column("checkup_time", sa.types.DateTime(timezone=True), default=datetime.utcnow),
        sa.Column("api_response", sa.types.JSON, nullable=False),  
    )

    # Create tables only if they don't already exist
    meta.create_all(engine)
except Exception as e:
    print(f"Error: {e}")

def insert_data_into_channel_metadata_table(records: list[dict]):
    """
    Insert data into the channel_metadata table in the database. 
    Argument is a list of dictionaries (key-value pairs) named records.
    """
    # Create a prepared statement to insert data into the table
    stmt = sa.insert(channel_metadata).values(records)
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()