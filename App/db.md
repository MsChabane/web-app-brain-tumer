# Database Setup (`db.py`)

This page describes the database configuration and session management for the FastAPI application using **SQLModel** and **SQLAlchemy AsyncIO**.

---

## 1. Database Engine

We create an asynchronous database engine using SQLAlchemy and the project’s database URL from settings.

```python
from sqlalchemy.ext.asyncio import create_async_engine
from App.settings import setting

engine = create_async_engine(
    setting.DATABASE_URL,
    execution_options={"prepared_statement_cache_size": 0}
)
```

## 2. Database Session 
We create asyncsession .

```python 
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

```





