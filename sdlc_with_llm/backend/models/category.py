"""Category model for IT Support Portal."""
from sqlalchemy import Column, Integer, String, Text
from backend.database.connection import Base


class Category(Base):
    """
    Category model for ticket categorization.

    Attributes:
        id: Primary key
        name: Category name (e.g., "Hardware", "Software", "Network")
        description: Detailed description of the category
        sla_hours: Service Level Agreement hours for this category
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    sla_hours = Column(Integer, nullable=False, default=24)

    def __repr__(self) -> str:
        return f"<Category(id={self.id}, name='{self.name}', sla_hours={self.sla_hours})>"
