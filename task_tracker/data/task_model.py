from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapper
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from task_tracker.data.base import Base
from task_tracker.data.user_current_task import UserCurrentTask


class Task(Base):
    __tablename__ = "tasks"
    id: Mapper[int] = mapped_column(primary_key=True)
    title: Mapper[str] = mapped_column(String(50), nullable=False)
    description: Mapper[str] = mapped_column(String(256), nullable=False)
    state: Mapper[str] = mapped_column(String(50), nullable=False)
    user_current_tasks: Mapper[List[UserCurrentTask]] = relationship(back_populates="task")