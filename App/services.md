# UserServices

Service class responsible for managing **User** operations in the database.

## Methods

### `change_password(user: User, new_password: str, session: AsyncSession)`
- **Purpose:** Update the password of a user.
- **Input:** `User` object, new password string, database session.
- **Operation:** Hashes the new password, updates the user object, adds it to session.
- **Output:** Returns updated `User` object (not committed).

### `get(user_id: str, session: AsyncSession)`
- **Purpose:** Fetch a user by their ID.
- **Input:** User ID and database session.
- **Output:** Returns the `User` object or `None` if not found.

### `get_by_phone_number(phone_number: str, session: AsyncSession)`
- **Purpose:** Fetch a user by phone number.
- **Input:** Phone number string and database session.
- **Output:** Returns the `User` object or `None` if not found.

### `check_user_exist(phone_number: str, session: AsyncSession)`
- **Purpose:** Check if a user exists based on phone number.
- **Output:** Returns `True` if user exists, `False` otherwise.

### `add(user_data: UserCreate, session: AsyncSession)`
- **Purpose:** Add a new user to the database.
- **Input:** `UserCreate` schema and database session.
- **Operation:** Hashes the password, creates a `User` object, adds it to session.
- **Output:** Returns the created `User` object (not committed).

### `delete(user: User, session: AsyncSession)`
- **Purpose:** Delete a user from the database.
- **Input:** `User` object and database session.
- **Operation:** Removes the user from the session.

### `get_all(session: AsyncSession, page: int = 1, limit: int = 100)`
- **Purpose:** Fetch all users with pagination.
- **Input:** Database session, page number, limit per page.
- **Output:** Returns a list of `User` objects.
---
# AdminServices

Service class responsible for retrieving total counts of users, doctors, and patients.

## Methods

### `_get_totat_for(model: SQLModel, session: AsyncSession) -> int`
- **Purpose:** Internal helper to count the total rows in a table.
- **Input:** SQLModel class (`User`, `Doctor`, or `Patient`) and database session.
- **Output:** Returns the total count of records for the given model.

### `get_total_users(session: AsyncSession) -> int`
- **Purpose:** Get the total number of users.
- **Input:** Database session.
- **Output:** Returns total count of `User` records.

### `get_total_patients(session: AsyncSession) -> int`
- **Purpose:** Get the total number of patients.
- **Input:** Database session.
- **Output:** Returns total count of `Patient` records.

### `get_total_doctors(session: AsyncSession) -> int`
- **Purpose:** Get the total number of doctors.
- **Input:** Database session.
- **Output:** Returns total count of `Doctor` records.


