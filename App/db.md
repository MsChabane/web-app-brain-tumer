# Database Configuration (`db.py`)

This page describes the database setup and session management for the FastAPI application using **SQLModel** and **SQLAlchemy AsyncIO**.

---

## 1. Database Engine

An asynchronous database engine is created using SQLAlchemy and the database URL from settings.

```python
from sqlalchemy.ext.asyncio import create_async_engine
from App.settings import setting

engine = create_async_engine(
    setting.DATABASE_URL,
    execution_options={"prepared_statement_cache_size": 0}
)
```

# 2. Async Session
-------------

We define an asynchronous sessionmaker to manage database sessions.
```python
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

```

# 3.Initialize Database (`init_db`)
-------------------------------

This function creates all tables defined in the models asynchronously.
