from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
)

from .meta import Base


class Show(Base):
    __tablename__ = 'show'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    description = Column(Text)
    artist = Column(Text)
    time = Column(DateTime)


Index('time', Show.time, unique=True, mysql_length=255)
