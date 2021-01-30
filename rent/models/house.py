from sqlalchemy import Column, String, Date, text

from rent.db import Base


class House(Base):

    __tablename__ = 'house'

    id = Column(String(16), nullable=False, primary_key=True)
    date = Column(Date, nullable=False, server_default=text('(CURRENT_DATE)'))

    def __repr__(self):
        return str([getattr(self, c.name, None) for c in self.__table__.c])
