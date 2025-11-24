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


# DoctorServices

Service class responsible for managing doctors and evaluating patients based on their symptoms.

## Methods

### `update(doctor: Doctor, doctor_data: DoctorUpdate, session: AsyncSession)`
- **Purpose:** Update a doctor's information with the provided data.
- **Input:** `Doctor` instance, `DoctorUpdate` data, database session.
- **Output:** Updated `Doctor` object.

### `get(doctor_id: str, session: AsyncSession) -> Doctor`
- **Purpose:** Retrieve a doctor by ID.
- **Input:** Doctor ID, database session.
- **Output:** `Doctor` object if found.

### `get_all(session: AsyncSession, page: int = 1, limit: int = 100)`
- **Purpose:** Retrieve all doctors with pagination.
- **Input:** Database session, page number, limit per page.
- **Output:** List of `Doctor` objects.

### `add(doctor_data: DoctorCreate, session: AsyncSession)`
- **Purpose:** Add a new doctor to the database.
- **Input:** `DoctorCreate` data, database session.
- **Output:** Added `Doctor` object.

### `get_by_user_id(user_id: str, session: AsyncSession)`
- **Purpose:** Retrieve a doctor by their associated user ID.
- **Input:** User ID, database session.
- **Output:** `Doctor` object if found.

### `detete(doctor: Doctor, session: AsyncSession)`
- **Purpose:** Delete a doctor and dissociate all their patients.
- **Input:** `Doctor` object, database session.
- **Output:** Doctor removed, patients' `doctor_id` set to `None`.

### `to_check(patient: Patient, latest_symptoms: LatestSymptoms) -> PatientUpdateStatus | None`
- **Purpose:** Evaluate a patient’s status based on latest symptoms and patient attributes.
- **Input:** `Patient` object, `LatestSymptoms` object.
- **Output:** `PatientUpdateStatus` if any rule matches, otherwise `None`.

#### Rules for Patient Evaluation

1. **High Risk (Tumor = 1, Hospitalisation = 2, Final State = T):**
   - `age > 62`
   - `antecedents > 0`
   - `seizures == 2`
   - `drowsiness == 1`
   - `radio_image.type >= 2`

2. **Moderate Risk (Tumor = 1, Hospitalisation = 1, Final State = D):**
   - `pressure >= 2`
   - `fatigue == 2`
   - `memory_pb >= 2`

3. **High Risk (Tumor = 1, Hospitalisation = 2, Final State = T):**
   - `balance_loss == 1`
   - `muscle >= 2`
   - `age > 50`

4. **High Risk (Tumor = 1, Hospitalisation = 2, Final State = T):**
   - `judgment_degradation >= 2`
   - `sense_degradation >= 2`
   - `seizures == TC`

5. **Low Risk (Tumor = 0, Hospitalisation = 0, Final State = N):**
   - `seizures == M`
   - `fatigue <= 1`
   - `radio_image.type == 0`

6. **High Risk (Tumor = 1, Hospitalisation = 2, Final State = T):**
   - `drowsiness == 2`
   - `pressure >= 2`
   - `gender > 55`

7. **Moderate Risk (Tumor = 1, Hospitalisation = 1, Final State = D):**
   - `fatigue == 2`
   - `memory_pb >= 1`
   - `seizures in [TC, S]`

8. **Serious Risk (Tumor = 1, Hospitalisation = 3, Final State = R):**
   - `muscle >= 2`
   - `swallowing >= 2`
   - `radio_image.type >= 2`
