from sqlalchemy import select
from task_tracker.data.db import Session
from task_tracker.data.model import User, Task


# Handle user
def handle_user(session, username: str, password: str):
    print("handle_user()")
    print(f"username: {username}")
    print(f"password: {password}")
    # Verify user credentials
    payload = {}
    user = session.scalar(select(User).where(User.username == username))
    if user:
        if password == user.password:
            payload["user"] = user
            payload["status"] = "User verified."
            # TODO: log record of user login
            # TODO: User should handle login
            # TODO: set logged in flag for user
    else:
        payload["user"] = None
        payload["status"] = "Credentials not found."
    print(user.password)

    return payload

