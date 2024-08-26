from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey
from sqlalchemy.sql.expression import text
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    contents = Column(String, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
