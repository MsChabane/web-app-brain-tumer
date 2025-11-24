# Authentication & Access Control (`auth.py`)

This page describes the authentication and role-based access control logic for the FastAPI application using **HTTPBearer tokens**.

---

## 1. AccessTokenChecker Class

`AccessTokenChecker` extends FastAPI’s `HTTPBearer` to validate JWT tokens in requests.

```python
from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request, status
from ..utils import decode_token

class AccessTokenChecker(HTTPBearer):
    def __init__(self):
        super().__init__(auto_error=False)
        
    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        
        if creds is None:
            raise HTTPException(
                detail="No access token provided",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        token = creds.credentials
        token_data = decode_token(token)
        if token_data is None:
            raise HTTPException(
                detail="Invalid token.",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
    
        return token_data
```
**Explanation:**
*   `auto_error=False` prevents automatic 401 errors, allowing custom handling.
    
*   Checks if the request contains a token and verifies it using `decode_token`.
    
*   Raises `HTTPException` if no token or invalid token is provided.


# 2. Dependency: `acees_token_checker`
```python
from typing import Annotated
from fastapi import Depends
from ..schemas.authSchemas import Token_Data

acees_token_checker = Annotated[Token_Data, Depends(AccessTokenChecker())]
```
# 3. Get Current User
```python
from ..services.UserServices import UserServices
from ..models.UserModel import User
from .common import db_dependency

async def get_current_user(token_data: acees_token_checker, session: db_dependency) -> User:
    user = await UserServices().get(token_data.user_id, session)
    if not user:
        raise HTTPException(detail='User not found', status_code=404)
    return user

current_user = Depends(get_current_user)

```
**Explanation:**
*   Retrieves the currently authenticated user from the database.
    
*   Raises `404` if the user does not exist.

# 4. Role-Based Access Control

```python
from fastapi import HTTPException, status
from ..schemas.types import Role

def role_required(required_role: str) -> User:
    def wrapper(user=current_user):
        if user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        return user
    return wrapper

only_admins = Depends(role_required(Role.ADMIN))
only_doctors = Depends(role_required(Role.DOCTOR))
only_patients = Depends(role_required(Role.PATIENT))

```
**Explanation:**
*   `role_required` checks if the current user has the required role.
    
*   Raises `403 Forbidden` if the role does not match.
    
*   Predefined dependencies for common roles: `only_admins`, `only_doctors`, `only_patients`.

# Database Dependency (`common.py`)

This page describes the common database dependency used in the FastAPI application to provide **async database sessions** to endpoints.

---

## 1. Import Dependencies

```python
from fastapi import Depends
from typing import Annotated
from ..db.db import get_session, AsyncSession
```
*   `Depends` is used to declare FastAPI dependencies.
    
*   `AsyncSession` is the SQLAlchemy asynchronous session class.
    
*   `get_session` is the function that provides an async database session.

2. Database Dependency
----------------------
```python 
db_dependency = Annotated[AsyncSession, Depends(get_session)]
```

*   `db_dependency` is a **type-annotated dependency** for FastAPI endpoints.
    
*   Allows endpoints to automatically receive a ready-to-use `AsyncSession`