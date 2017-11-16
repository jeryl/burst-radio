from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    DateTime,
)

from .meta import Base


class NowPlaying(Base):
    """LOL this bullshit table"""
    __tablename__ = 'now_playing'
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    show_id = Column(Integer)


Index('now_playing_time', NowPlaying.time)
