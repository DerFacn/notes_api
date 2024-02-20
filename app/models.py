from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey
from typing import List

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    uuid: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    password: Mapped[str]

    notes: Mapped[List["Note"]] = relationship(back_populates='user', cascade='all, delete-orphan')

    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Note(Base):
    __tablename__ = 'notes'
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    user_uuid: Mapped[str] = mapped_column(ForeignKey('users.uuid'))
    user: Mapped[List["User"]] = relationship(back_populates='notes')
