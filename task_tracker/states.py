
STATES = [
    {
        "state": "created",
        "description": "Task has been created.",
        "follows": []
    },
    {
        "state": "todo",
        "description": "Task is in backlog.",
        "follows": ["created"]
    },
    {
        "state": "in_progress",
        "description": "Task is in progress.",
        "follows": ["todo", "paused"]
    },
    {
        "state": "paused",
        "description": "Task is paused.",
        "follows": ["in_progress", "in_review"]
    },
    {
        "state": "in_review",
        "description": "Task is in review.",
        "follows": ["in_progress"]
    },
    {
        "state": "for_approval",
        "description": "Task is waiting for review and approval.",
        "follows": ["in_review"]
    },
    {
        "state": "done",
        "description": "Task is done.",
        "follows": ["for_approval"]
    }
]
