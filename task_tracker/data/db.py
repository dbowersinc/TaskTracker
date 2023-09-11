from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite+pysqlite:///task_tracker/data/task_tracker.db', echo=True)
Session = sessionmaker(bind=engine)