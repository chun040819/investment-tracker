from __future__ import annotations

import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Ensure project root is on the path when running Alembic.
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.core.config import settings  # noqa: E402
from app.db.base import Base  # noqa: E402
# Import all models so Alembic can autogenerate metadata.
from app.models.portfolio import Portfolio, CostMethod  # noqa: F401,E402
from app.models.account import Account  # noqa: F401,E402
from app.models.asset import Asset, AssetType  # noqa: F401,E402
from app.models.trade import Trade, TradeSide  # noqa: F401,E402
from app.models.cash_transaction import CashTransaction, CashTxnType  # noqa: F401,E402
from app.models.corporate_action import CorporateAction, CorporateActionType  # noqa: F401,E402
from app.models.price_history import PriceHistory  # noqa: F401,E402
from app.models.fx_rate import FXRate  # noqa: F401,E402
from app.models.tag import Tag  # noqa: F401,E402
from app.models.position_snapshot import PositionSnapshot  # noqa: F401,E402
from app.models.tax_lot import TaxLot  # noqa: F401,E402

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
