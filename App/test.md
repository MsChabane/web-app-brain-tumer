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
```

# **test_auth.py Wiki**

## **Purpose**
Tests the **authentication and user management endpoints** of the FastAPI app, including:

- Login functionality
- Role-based access control
- Admin creation
- User listing
- Profile endpoints for different roles

---

## **Test Functions**

### **1. `test_login`**
- **Purpose:** Tests the `/auth/login` endpoint.
- **Setup:** Uses `fake_login_user` and `test_client`.
- **Test checks:**
  - Status code is 200.
  - Response contains `access_token`.
  - User role matches the expected role (doctor in this case).

---

### **2. `test_create_admin_by_non_admin`**
- **Purpose:** Ensures non-admin users **cannot create admin accounts**.
- **Clients used:**
  - `client_with_auth_doctor`
  - `client_with_auth_patient`
- **Expected outcome:** 
  - Status code 403
  - Error detail: `"Access denied"`

---

### **3. `test_create_admin_by_admin_with_user_exist`**
- **Purpose:** Tests admin trying to create an admin when the user **already exists**.
- **Fixtures:** `client_with_auth_admin`, `fake_user_exist_true`
- **Expected outcome:** 
  - Status code 400
  - Error detail: `"User is already exist"`

---

### **4. `test_create_admin_by_admin`**
- **Purpose:** Tests admin creating a new admin when the user **does not exist**.
- **Fixtures:** `client_with_auth_admin`, `fake_user_exist_false`
- **Expected outcome:** 
  - Status code 201 (Created)

---

### **5. `test_get_all_users_admin`**
- **Purpose:** Tests `/auth/users/all` endpoint for admin.
- **Fixtures:** `client_with_auth_admin`, `mock_session`, `fake_user_list`
- **Checks:**
  - Status code 200
  - Response is a list with correct length
  - Ensures `user_services.get_all` is called with correct arguments (`session`, `page`, `limit`)

---

### **6. `test_profile_patient`**
- **Purpose:** Tests `/auth/profile` for a **patient**.
- **Checks:**
  - Status code 200
  - Response contains `id`, `phone_number`, `role`
  - Role is `"patient"`

---

### **7. `test_profile_doctor`**
- **Purpose:** Tests `/auth/profile` for a **doctor**.
- **Checks:**
  - Status code 200
  - Response contains `id`, `phone_number`, `role`
  - Role is `"doctor"`

---

### **8. `test_profile_admin`**
- **Purpose:** Tests `/auth/profile` for an **admin**.
- **Checks:**
  - Status code 200
  - Response contains `id`, `phone_number`, `role`
  - Role is `"admin"`

---

## **Key Concepts**
- **Role-based testing:** Separate clients simulate different user roles.
- **Dependency overrides:** `conftest.py` fixtures replace real authentication and database calls.
- **Use of mock data:** `fake_user_exist_true/false` and `fake_user_list` control test scenarios without touching the real database.
- **HTTP status codes:** 200 (success), 201 (created), 400 (user exists), 403 (access denied)
