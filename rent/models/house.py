from sqlalchemy import Column, String, Date, func

from rent.db import Base


class House(Base):

    __tablename__ = 'house'

    id = Column(String(16), nullable=False, primary_key=True)
    date = Column(Date, nullable=False, primary_key=True, server_default=func.sysdate())

    def __repr__(self):
        return str([getattr(self, c.name, None) for c in self.__table__.c])
