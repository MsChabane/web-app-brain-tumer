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
