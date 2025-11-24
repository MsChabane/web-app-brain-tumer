# Types (`types.py`)

This file defines all the enumerations used across models and schemas.

| Enum | Values | Description / Usage |
|------|--------|-------------------|
| `Role` | `"admin"`, `"doctor"`, `"patient"` | Defines the role of a user in the system. |
| `FinalStateEnum` | `"T"`, `"D"`, `"R"`, `"N"` | Represents the final state of a patient (used in `Patient` model). |
| `Gender` | `"M"`, `"F"` | Represents patient gender. |
| `Binary` | `0`, `1` | Represents a binary choice or status (e.g., presence/absence of a symptom). |
| `Three_Classes` | `0`, `1`, `2` | Represents categorical values with three options (used in symptoms). |
| `Four_Classes` | `0`, `1`, `2`, `3` | Represents categorical values with four options (used in symptoms). |
| `Seizures` | `"M"`, `"TC"`, `"S"`, `"C"` | Represents types of seizures for general symptoms. |


# Authentication Schemas (`authSchemas.py`)

Defines Pydantic models for authentication and token handling.

| Schema | Fields | Description / Usage |
|--------|--------|-------------------|
| `Token` | `access_token: str`<br>`type: str = 'Bearer'`<br>`role: str` | Represents an access token returned after login, including the user role. |
| `Token_Data` | `user_id: str` | Represents the data encoded in the access token (user ID). |
| `Change_password` | `password: str` | Represents the payload to change a user's password. |


# User Schemas (`UserSchemas.py`)

Defines Pydantic models for user data, authentication, and validation.

| Schema | Fields | Description / Usage |
|--------|--------|-------------------|
| `UserBase` | `phone_number: str` | Base schema for a user with phone number validation for Algerian numbers. |
| `UserLogin` | Inherits `UserBase`<br>`password: str` | Payload for user login. |
| `UserUpdate` | `password: str` | Payload to update user password. |
| `UserCreate` | Inherits `UserLogin`<br>`role: str` | Payload to create a new user with role. |
| `UserOut` | `id: UUID`<br>`phone_number: str`<br>`role: str` | Schema for user data returned in responses. |

# Doctor Schemas (`DoctorSchemas.py`)

Defines Pydantic models for doctor data management.

| Schema | Fields | Description / Usage |
|--------|--------|-------------------|
| `DoctorBase` | `name: str`<br>`specialty: str`<br>`years_experience: int` | Base schema for doctor details. |
| `DoctorCreate` | Inherits `DoctorBase`<br>`user_id: UUID` | Payload for creating a doctor linked to a user. |
| `DoctorUpdate` | `name: Optional[str]`<br>`specialty: Optional[str]`<br>`years_experience: Optional[int]` | Payload for updating doctor details (partial updates allowed). |
| `DoctorOut` | Inherits `DoctorBase`<br>`id: UUID` | Schema for doctor data returned in responses. |
