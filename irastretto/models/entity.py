""":mod:'irastretto.models.entity'

"""
from sqlalchemy import (Column, String, Integer, BigInteger, Boolean, DateTime)
from ..db.orm import Base


class Entity(Base):
    """Extracted Entity data.

    entity_id: entity id.
    data_id: platform$data_id to hashed id.
    platform: origin source platform.
    author: origin author.
    source: source url.
    description: description from source.
    """
    __tablename__ = 'entity'

    entity_id = Column(BigInteger,
                       primary_key=True)  # must change to Integer before using sqlite.
    data_id = Column(String,
                     unique=True)
    platform = Column(String, nullable=False)
    author = Column(String, nullable=False)
    source = Column(String, nullable=False)
    description = Column(String, nullable=False)
