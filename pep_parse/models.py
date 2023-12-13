from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, declared_attr, relationship

from pep_parse.settings import STRING_LENGTH


class Base:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=Base)


class Status(Base):
    """PEP document status db model."""
    status = Column(String(STRING_LENGTH), unique=True)
    peps = relationship('Pep', back_populates='status')

    def __repr__(self):
        return self.status


class Pep(Base):
    """PEP document db model."""
    pep_number = Column(Integer, unique=True, nullable=False)
    title = Column(String(STRING_LENGTH), nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    status = relationship('Status', back_populates='peps')

    def __repr__(self):
        return f'{self.pep_number} - {self.title}'
