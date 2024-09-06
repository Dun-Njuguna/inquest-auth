import sys
import os
from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# Add the src directory to sys.path for module imports
sys.path = ['', '..'] + sys.path[1:]

# Import Base from the models module
from src.models.base import Base

# Import the SQLAlchemy models
from src.models.user_model import User
from src.models.role_model import Role
from src.models.token_model import Token

# Load environment variables from the .env file
load_dotenv()

# Fetch database configuration from environment variables
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Construct the database URL for SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Set target_metadata to include all models registered with Base
target_metadata = Base.metadata

# Create the SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=pool.NullPool
)

def run_migrations_offline():
    """
    Run migrations in 'offline' mode.
    
    In offline mode, Alembic generates SQL scripts for migrations
    without connecting to the database. The SQL is output to a file
    or stdout, allowing you to apply it manually.
    """
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """
    Run migrations in 'online' mode.
    
    In online mode, Alembic connects to the database and applies
    the migrations directly.
    """
    connectable = engine

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

# Determine if Alembic is running in offline or online mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
