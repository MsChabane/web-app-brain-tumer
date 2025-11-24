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

# Patient Schemas (`PatientSchemas.py`)

Defines Pydantic models for patient data, status, and response formatting.

| Schema | Fields | Description / Usage |
|--------|--------|-------------------|
| `PatientBase` | `name: str`<br>`surname: str`<br>`age: int`<br>`gender: Gender`<br>`antecedents: Four_Classes` | Base schema for patient details with age validation (1–130). |
| `PatientCreate` | Inherits `PatientBase`<br>`user_id: UUID` | Payload for creating a patient linked to a user. |
| `PatientUpdateStatus` | `tumor_status: Binary | None`<br>`hospitalisation: Four_Classes | None`<br>`final_state: FinalStateEnum | None` | Payload for updating patient’s clinical status. |
| `PatientUpdate` | `name: Optional[str]`<br>`surname: Optional[str]`<br>`age: Optional[int]`<br>`gender: Optional[Gender]`<br>`antecedents: Optional[Four_Classes]` | Payload for updating patient details (partial updates allowed). |
| `PatientOut` | Inherits `PatientBase`<br>`id: UUID`<br>`tumor_status: Binary | None`<br>`hospitalisation: Four_Classes | None`<br>`final_state: FinalStateEnum | None`<br>`doctor: DoctorOut | None` | Schema for patient data returned in responses, including assigned doctor info. |

# General Symptoms Schemas (`GeneralSymptomsSchemas.py`)

Defines Pydantic models for handling general symptoms of patients.

| Schema | Fields | Description / Usage |
|--------|--------|-------------------|
| `GeneralSymptomsBase` | `headaches: Three_Classes`<br>`seizures: Seizures`<br>`fatigue: Three_Classes`<br>`drowsiness: Three_Classes`<br>`sleep_pb: Three_Classes`<br>`memory_pb: Three_Classes` | Base schema for general symptoms. |
| `GeneralSymptomsCreate` | Inherits `GeneralSymptomsBase`<br>`patient_id: UUID` | Payload for adding general symptoms to a patient. |
| `GeneralSymptomsOut` | Inherits `GeneralSymptomsBase`<br>`id: UUID`<br>`created_at: datetime` | Schema for returning general symptoms, including timestamp. |
| `GeneralSymptomsUpdate` | Optional fields matching `GeneralSymptomsBase` | Payload for updating general symptoms (partial updates allowed). |

# Specific Symptoms Schemas (`SpecificSymptomsSchemas.py`)

Defines Pydantic models for handling specific symptoms of patients.

| Schema | Fields | Description / Usage |
|--------|--------|-------------------|
| `SpecificSymptomsBase` | `pressure: Four_Classes`<br>`balance_loss: Binary`<br>`judgment_degradation: Four_Classes`<br>`sense_degradation: Four_Classes`<br>`lactation: Three_Classes`<br>`swallowing: Four_Classes`<br>`muscle: Four_Classes` | Base schema for specific symptoms. |
| `SpecificSymptomsCreate` | Inherits `SpecificSymptomsBase`<br>`patient_id: UUID` | Payload for adding specific symptoms to a patient. |
| `SpecificSymptomsOut` | Inherits `SpecificSymptomsBase`<br>`id: UUID`<br>`created_at: datetime` | Schema for returning specific symptoms, including timestamp. |
| `SpecificSymptomsUpdate` | Optional fields matching `SpecificSymptomsBase` | Payload for updating specific symptoms (partial updates allowed). |

# Radio Image Schemas (`RadioImageSchemas.py`)

Defines Pydantic models for handling radiological images of patients.

| Schema | Fields | Description / Usage |
|--------|--------|-------------------|
| `RadioImageBase` | `type: int` | Base schema for radiological image type. |
| `RadioImageCreate` | Inherits `RadioImageBase`<br>`patient_id: UUID` | Payload for adding a radiological image to a patient. |
| `RadioImageOut` | Inherits `RadioImageBase`<br>`id: UUID`<br>`created_at: datetime` | Schema for returning a radiological image, including timestamp. |
