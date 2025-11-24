# 1.Auth Routes

| Route | Method | Purpose / Description | Response / Result |
|-------|--------|---------------------|-----------------|
| `/login` | POST | Authenticate a user with phone number and password. | Returns JWT token and user role. `404` if user not found, `400` if password invalid. |
| `/create-admin` | POST | Create a new admin user. **Only accessible by admins.** | Returns created admin user details. `400` if user already exists. |
| `/users/all` | GET | Retrieve a paginated list of all users. **Admin only.** | Returns list of users (`UserOut`). |
| `/profile` | GET | Get the profile of the current logged-in user. | Returns current user details (`UserOut`). |
| `/user/change-password` | POST | Change the password of the current user. | Returns confirmation message `Password Changed`. |
| `/users/admin/{user_id}` | DELETE | Delete an admin user by ID. **Admin only.** Cannot delete self. | Returns confirmation message `deleted`. `400` if user not found, not admin, or trying to delete self. |
