# 1.Auth Routes

| Route | Method | Purpose / Description | Response / Result |
|-------|--------|---------------------|-----------------|
| `/auth/login` | POST | Authenticate a user with phone number and password. | Returns JWT token and user role. `404` if user not found, `400` if password invalid. |
| `/auth/create-admin` | POST | Create a new admin user. **Only accessible by admins.** | Returns created admin user details. `400` if user already exists. |
| `/auth/users/all` | GET | Retrieve a paginated list of all users. **Admin only.** | Returns list of users (`UserOut`). |
| `/auth/profile` | GET | Get the profile of the current logged-in user. | Returns current user details (`UserOut`). |
| `/auth/user/change-password` | POST | Change the password of the current user. | Returns confirmation message `Password Changed`. |
| `/auth/users/admin/{user_id}` | DELETE | Delete an admin user by ID. **Admin only.** Cannot delete self. | Returns confirmation message `deleted`. `400` if user not found, not admin, or trying to delete self. |


# Dashboard Routes

| Route | Method | Purpose / Description | Response / Result |
|-------|--------|---------------------|-----------------|
| `/total-dectors` | GET | Get total number of doctors. **Admin only.** | Returns total doctors as integer in a message object. |
| `/total-patients` | GET | Get total number of patients. **Admin only.** | Returns total patients as integer in a message object. |
| `/total-users` | GET | Get total number of users. **Admin only.** | Returns total users as integer in a message object. |
| `/total` | GET | Get all totals (users, doctors, patients) in one response. **Admin only.** | Returns a `Total_insights` object containing `total_doctors`, `total_users`, and `total_patients`. |


 
# Doctor Routes (`/doctor` prefix)

| Route | Method | Purpose / Description | Response / Result |
|-------|--------|---------------------|-----------------|
| `/doctor/new-doctor` | POST | Create a new doctor. **Admin only.** | Returns created doctor details (`DoctorOut`). `400` if user already exists. |
| `/doctor/all` | GET | Get all doctors. **Admin only.** | Returns list of doctors. Supports pagination (`page` and `limit`). |
| `/doctor/me` | GET | Get the profile of the current logged-in doctor. **Doctor only.** | Returns doctor details (`DoctorOut`). |
| `/doctor/get-patients` | GET | Get all patients assigned to the current doctor. **Doctor only.** | Returns list of patients (`PatientOut`). `404` if doctor not found. |
| `/doctor/{id}` | GET | Get a doctor by ID. | Returns doctor details (`DoctorOut`). |
| `/doctor/{id}` | PUT | Update doctor information by ID. | Returns updated doctor details (`DoctorOut`). `404` if doctor not found. |
| `/doctor/check/{patient_id}` | POST | Doctor checks a patient and updates their state. **Doctor only.** | Returns updated patient info (`PatientOut`). `404` if patient not found, `400` if doctor not assigned to patient. |
| `/doctor/{id}` | DELETE | Delete a doctor by ID. **Admin only.** | Returns confirmation message `deleted`. `404` if doctor not found. |

