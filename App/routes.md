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
| `/dashboard/total-dectors` | GET | Get total number of doctors. **Admin only.** | Returns total doctors as integer in a message object. |
| `/dashboard/total-patients` | GET | Get total number of patients. **Admin only.** | Returns total patients as integer in a message object. |
| `/dashboard/total-users` | GET | Get total number of users. **Admin only.** | Returns total users as integer in a message object. |
| `/dashboard/total` | GET | Get all totals (users, doctors, patients) in one response. **Admin only.** | Returns a `Total_insights` object containing `total_doctors`, `total_users`, and `total_patients`. |


 
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

# Patient Routes (`/patient` prefix)

| Route | Method | Purpose / Description | Response / Result |
|-------|--------|---------------------|-----------------|
| `/patient/new-patient` | POST | Create a new patient. **Admin only.** | Returns created patient details (`PatientOut`). `400` if user already exists. |
| `/patient/all` | GET | Get all patients. **Admin only.** | Returns list of patients with optional pagination (`page`, `limit`). |
| `/patient/me` | GET | Get the profile of the current logged-in patient. **Patient only.** | Returns patient details (`PatientOut`). |
| `/patient/get-latest-symptoms` | GET | Get latest symptom updates for the current patient. **Patient only.** | Returns `LatestSymptoms`. `404` if patient not found. |
| `/patient/no-associated` | GET | Get patients not associated with any doctor. | Returns list of patients (`PatientOut`). |
| `/patient/{patient_id}/get-all-symptoms` | GET | Get all symptoms of a patient. **Doctor only.** | Returns `AllSymptoms`. `404` if patient not found, `403` if doctor not assigned. |
| `/patient/{patient_id}` | GET | Get a patient by ID. | Returns patient details (`PatientOut`). |
| `/patient/{patient_id}/add-general-symptoms` | POST | Add general symptoms for a patient. **Doctor only.** | Returns `GeneralSymptomsOut`. `404` if patient not found, `403` if doctor not assigned. |
| `/patient/{patient_id}/add-specific-symptoms` | POST | Add specific symptoms for a patient. **Doctor only.** | Returns `SpecificSymptomsOut`. `404` if patient not found, `403` if doctor not assigned. |
| `/patient/{patient_id}/add-radioimage-symptoms` | POST | Add radiology image for a patient. **Doctor only.** | Returns `RadioImageOut`. `404` if patient not found, `403` if doctor not assigned. |
| `/patient/{patient_id}/associate-to/{doctor_id}` | POST | Associate a patient to a doctor. **Admin only.** | Returns updated patient (`PatientOut`). `404` if patient or doctor not found. |
| `/patient/{id}` | PUT | Update patient information. **Admin only.** | Returns updated patient (`PatientOut`). `404` if patient not found. |
| `/patient/general-symptoms/{id}` | PUT | Update general symptoms by ID. | Returns updated `GeneralSymptomsOut`. `404` if not found. |
| `/patient/specific-symptoms/{id}` | PUT | Update specific symptoms by ID. | Returns updated `SpecificSymptomsOut`. `404` if not found. |
| `/patient/radio-image/{id}` | PUT | Update radiology image by ID. | Returns updated `RadioImageOut`. `404` if not found. |
| `/patient/{id}` | DELETE | Delete a patient and its user account. | Returns confirmation message `deleted`. `404` if patient not found. |


# Main / Frontend Pages Routes

| Route | Method | Purpose / Description | Response / Result |
|-------|--------|---------------------|-----------------|
| `/auth/login` | GET | Serve the login page. | Returns `login.html` as HTML response. |
| `/admin` | GET | Serve the admin dashboard page. | Returns `admin.html` as HTML response. |
| `/doctor` | GET | Serve the doctor dashboard page. | Returns `doctor.html` as HTML response. |
| `/patient` | GET | Serve the patient dashboard page. | Returns `patient.html` as HTML response. |
| `/details/{patient_id}` | GET | Serve the patient detail page for a given patient ID. | Returns `detail.html` as HTML response. |
