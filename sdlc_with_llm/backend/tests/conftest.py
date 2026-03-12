"""Pytest configuration and fixtures for testing."""
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from datetime import datetime, timedelta
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from backend.database.connection import Base, get_db
from backend.models.user import User, UserRole
from backend.models.category import Category
from backend.models.ticket import Ticket, TicketStatus, TicketPriority
from backend.main import app


# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def test_engine():
    """Create test database engine."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        future=True
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def test_db(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    TestSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False
    )

    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def test_client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with database override."""

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_users(test_db: AsyncSession) -> dict:
    """Create sample users for testing."""
    users = {
        "end_user": User(
            id=1,
            username="john_doe",
            email="john@example.com",
            full_name="John Doe",
            role=UserRole.END_USER
        ),
        "agent": User(
            id=2,
            username="agent_smith",
            email="agent@example.com",
            full_name="Agent Smith",
            role=UserRole.SUPPORT_AGENT
        ),
        "admin": User(
            id=3,
            username="admin",
            email="admin@example.com",
            full_name="Admin User",
            role=UserRole.ADMIN
        ),
        "end_user2": User(
            id=4,
            username="jane_doe",
            email="jane@example.com",
            full_name="Jane Doe",
            role=UserRole.END_USER
        )
    }

    for user in users.values():
        test_db.add(user)

    await test_db.commit()

    # Refresh to get IDs
    for user in users.values():
        await test_db.refresh(user)

    return users


@pytest_asyncio.fixture
async def sample_categories(test_db: AsyncSession) -> dict:
    """Create sample categories for testing."""
    categories = {
        "hardware": Category(
            id=1,
            name="Hardware",
            description="Hardware issues",
            sla_hours=24
        ),
        "software": Category(
            id=2,
            name="Software",
            description="Software issues",
            sla_hours=48
        ),
        "network": Category(
            id=3,
            name="Network",
            description="Network issues",
            sla_hours=4
        )
    }

    for category in categories.values():
        test_db.add(category)

    await test_db.commit()

    # Refresh to get IDs
    for category in categories.values():
        await test_db.refresh(category)

    return categories


@pytest_asyncio.fixture
async def sample_tickets(test_db: AsyncSession, sample_users: dict, sample_categories: dict) -> dict:
    """Create sample tickets for testing."""
    now = datetime.utcnow()

    tickets = {
        "open_ticket": Ticket(
            id=1,
            title="Printer not working",
            description="Office printer HP-123 is not responding",
            status=TicketStatus.OPEN,
            priority=TicketPriority.MEDIUM,
            category_id=sample_categories["hardware"].id,
            submitted_by=sample_users["end_user"].id,
            created_at=now - timedelta(hours=2),
            updated_at=now - timedelta(hours=2),
            sla_breach=0
        ),
        "in_progress_ticket": Ticket(
            id=2,
            title="Cannot access email",
            description="Getting authentication error",
            status=TicketStatus.IN_PROGRESS,
            priority=TicketPriority.HIGH,
            category_id=sample_categories["software"].id,
            submitted_by=sample_users["end_user"].id,
            assigned_to=sample_users["agent"].id,
            created_at=now - timedelta(hours=5),
            updated_at=now - timedelta(hours=1),
            sla_breach=0
        ),
        "resolved_ticket": Ticket(
            id=3,
            title="Need software installation",
            description="Please install MS Office",
            status=TicketStatus.RESOLVED,
            priority=TicketPriority.LOW,
            category_id=sample_categories["software"].id,
            submitted_by=sample_users["end_user2"].id,
            assigned_to=sample_users["agent"].id,
            created_at=now - timedelta(days=1),
            updated_at=now - timedelta(hours=3),
            resolved_at=now - timedelta(hours=3),
            resolution_note="Software installed successfully",
            sla_breach=0
        ),
        "sla_breach_ticket": Ticket(
            id=4,
            title="Network outage",
            description="Cannot connect to internet",
            status=TicketStatus.OPEN,
            priority=TicketPriority.CRITICAL,
            category_id=sample_categories["network"].id,
            submitted_by=sample_users["end_user"].id,
            created_at=now - timedelta(hours=6),  # Network SLA is 4 hours
            updated_at=now - timedelta(hours=6),
            sla_breach=1
        )
    }

    for ticket in tickets.values():
        test_db.add(ticket)

    await test_db.commit()

    # Refresh to get IDs and relationships
    for ticket in tickets.values():
        await test_db.refresh(ticket)

    return tickets
