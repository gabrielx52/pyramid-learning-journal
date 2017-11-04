"""Database table models."""
from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Unicode
)

from .meta import Base


class Entry(Base):
    """Learning Journal database entry table model."""

    __tablename__ = 'Entry'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    body = Column(Unicode)
    creation_date = Column(DateTime, default=datetime.now())

    def to_dict(self):
        """Take all model attributes and render them as a dictionary."""
        return {'id': self.id,
                'title': self.title,
                'body': self.body,
                'creation_date': self.creation_date.strftime('%A, %d %B, %Y, %I:%M %p')
                }
