from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from task_tracker.data.base import Base
from task_tracker.data.task_model import Task
from task_tracker.data.user_current_task import UserCurrentTask


class User(Base):
    __tablename__ = "users"
    id: Mapper[int] = mapped_column(primary_key=True)
    username: Mapper[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapper[str] = mapped_column(String(256), nullable=False)
    user_current_tasks: Mapper[UserCurrentTask] = relationship(back_populates="user")
