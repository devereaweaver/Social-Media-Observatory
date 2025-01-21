# This script is used to create a schema for the database that will store the metadata
# of the Telegram channels
from config import config
import sqlalchemy as sa
from datetime import datetime


def insert_data_into_channel_metadata_table(records: list[dict]):
    """
    inserts data into the channel_metadata table
    """
    # Create a prepared SQL statement using the channel_metadata table object
    # this is instantiated below
    stmt = sa.insert(channel_metadata).values(records)

    # Initiate a connection with the database
    with engine.connect() as conn:
        conn.execute(stmt)
        conn.commit()  # Commit the transaction to the database


# Attempt to connect to the PostgreSQL database server w/credentials from config file
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

# Create a metadata object that acts as a container for database schema definitions
# (e.g. tables, columns, indexes, etc.)
meta = sa.MetaData()

# TODO: Place this code into a separate function after making sure the code
# is working properly for production
# Create a Table object that represents the channel_metadata table and associated metadata
channel_metadata = sa.Table(
    "channel_metadata",
    meta,
    sa.Column("channel_id", sa.types.BIGINT, primary_key=True),
    sa.Column("channel_name", sa.types.TEXT, unique=True),
    sa.Column("channel_title", sa.types.TEXT, default=None),
    sa.Column("channel_birthdate", sa.types.DateTime(timezone=True)),
    sa.Column("channel_bio", sa.types.TEXT, default=None),
    sa.Column("num_subscribers", sa.types.INTEGER, default=None),
    sa.Column("data_source", sa.types.TEXT, default="telegram-api"),
    sa.Column(
        "checkup_time", sa.types.DateTime(timezone=True), default=datetime.utcnow
    ),
    sa.Column("api_response", sa.types.JSON, nullable=False),
)

# Create new tables only if they don't already exist
meta.create_all(engine)
