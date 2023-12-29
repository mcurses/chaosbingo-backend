import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

# Define tables here with SQLAlchemy
prompts = sqlalchemy.Table(
    "prompts",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
)

# Add other tables (players, scores) similarly...

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

