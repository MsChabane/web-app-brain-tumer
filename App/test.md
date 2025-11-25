# **conftest.py Wiki**

## **Purpose**
This file sets up **fixtures and mocks** for testing the FastAPI application. It mainly:

1. Provides a **mock database session** (`AsyncSession`) to avoid touching the real database.
2. Mocks authentication for different user roles (`Admin`, `Doctor`, `Patient`) for endpoint testing.
3. Mocks **user service methods** (`get_by_phone_number`, `check_user_exist`, `get_all`) for isolated testing.

---

## **Fixtures**

### **1. `mock_session`**
- **Type:** `AsyncMock`
- **Purpose:** Simulates a SQLAlchemy/SQLModel async session.
- **Methods mocked:** `exec`, `commit`, `delete`, `add`.
- **Usage:** Used to override the real database session in tests.

---

### **2. `override_session`**
- **Purpose:** Automatically overrides `get_session` dependency in FastAPI app with `mock_session`.
- **Scope:** Autouse (applied automatically to all tests using the app).

---

### **3. `override_token_checker`**
- **Purpose:** Mocks `AccessTokenChecker` to return a fake token with a random user ID.
- **Usage:** Allows bypassing real JWT authentication during tests.

---

### **4. `make_user(role)`**
- **Purpose:** Helper function to create a `User` object with a specific role (`ADMIN`, `DOCTOR`, `PATIENT`).
- **Fields:** `id`, `phone_number`, `password`, `role`.

---

### **5. `client_with_auth_*` (Admin/Doctor/Patient)**
- **Purpose:** Returns a `TestClient` with a mocked authenticated user of a specific role.
- **How it works:** Overrides `get_current_user` dependency with a fake user object.

---

### **6. `fake_login_user`**
- **Purpose:** Mocks `user_services.get_by_phone_number` to return a pre-defined fake user.
- **Usage:** For testing login endpoints without accessing the real database.

---

### **7. `fake_user_exist_true` / `fake_user_exist_false`**
- **Purpose:** Mocks `user_services.check_user_exist` to always return `True` or `False`.
- **Usage:** To simulate scenarios where a user exists or does not exist.

---

### **8. `test_client`**
- **Purpose:** Provides a simple `TestClient` with token checker override.

---

### **9. `fake_user_list`**
- **Purpose:** Mocks `user_services.get_all` to return a predefined list of users.
- **Example returned data:** 
  ```json
  [
      {"id": "...", "phone_number": "0550112233", "role": "doctor"},
      {"id": "...", "phone_number": "0660223344", "role": "patient"}
  ]
