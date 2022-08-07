from enum import Enum

class Status(str, Enum):
    done = "Task Done"
    pending = "Task Pending"
    expired = "Task Expired"