"""
SQLAlchemy ORM models for FestSync.

All models should inherit from Base and follow naming conventions:
- Table names: plural snake_case (e.g., users, events)
- Columns: snake_case
- Relationships: camelCase
"""

from app.core.database import Base
from app.models.workspace import Workspace, WorkspaceMember

# Import models here
# from app.models.user import User
# from app.models.event import Event
# from app.models.task import Task
# from app.models.vendor import Vendor
# from app.models.budget import BudgetItem
# from app.models.guest import Guest
# from app.models.booking import Booking

__all__ = [
    "Base",
    "Workspace",
    "WorkspaceMember",
    # "User",
    # "Event",
    # "Task",
    # "Vendor",
    # "BudgetItem",
    # "Guest",
    # "Booking",
]
