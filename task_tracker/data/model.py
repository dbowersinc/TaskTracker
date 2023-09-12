from typing import List
from typing import Optional
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(256), nullable=False)
    task_id: Mapped[Optional[int]] = mapped_column(ForeignKey("tasks.id"), nullable=True)
    current_task: Mapped["Task"] = relationship(back_populates="user")
    user_task_state_records: Mapped[List["UserTaskStateRecord"]] = relationship(back_populates="user")


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(256), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    user: Mapped[List["User"]] = relationship(back_populates="current_task")
    user_task_state_records: Mapped[List["UserTaskStateRecord"]] = relationship(back_populates="task")


class UserTaskStateRecord(Base):
    __tablename__ = "user_task_state_records"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(String(50), nullable=False, default=datetime.utcnow)
    user: Mapped[User] = relationship(back_populates="user_task_state_records")
    task: Mapped[Task] = relationship(back_populates="user_task_state_records")

