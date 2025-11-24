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


# 2.Dependency: `acees_token_checker`