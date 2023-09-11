from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from task_tracker.data.base import Base
from task_tracker.data.task_model import Task
from task_tracker.data.user_model import User


class UserCurrentTask(Base):
    __tablename__ = "user_current_tasks"
    id: Mapper[int] = mapped_column(primary_key=True)
    user_id: Mapper[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapper[int] = mapped_column(ForeignKey("tasks.id"))
    user: Mapper[User] = relationship(back_populates="user_current_tasks")
    task: Mapper[Task] = relationship(back_populates="user_current_tasks")
