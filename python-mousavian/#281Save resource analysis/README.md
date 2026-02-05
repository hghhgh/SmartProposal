from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    DateTime,
    Enum,
    create_engine,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class ReferenceStatus(str, enum.Enum):
    valid = "valid"
    invalid = "invalid"
    unknown = "unknown"


class ReferenceResult(Base):
    __tablename__ = "reference_results"

    id = Column(BigInteger, primary_key=True)

    batch_id = Column(PG_UUID(as_uuid=True), nullable=False)

    ref_type = Column(String(50), nullable=False)
    ref_value = Column(Text, nullable=False)
    ref_target = Column(Text)

    status = Column(Enum(ReferenceStatus), nullable=False)

    error_code = Column(String(50))
    message = Column(Text)

    source = Column(String(50))

    checked_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)


# ---- database setup ----

DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/dbname"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db() -> None:
    Base.metadata.create_all(engine)
