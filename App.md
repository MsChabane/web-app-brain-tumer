# Project Entry Point

This file is the **main entry point** of the application. It initializes the FastAPI app, sets up routes, templates, and static files. All requests to the app start here.

## Parent Folder Structure

- `App/`
  - `main.py` ← **This file** (entry point)
  - `routes/` ← Contains all API route modules (auth, doctor, patient, dashboard)
  - `schemas/` ← Pydantic models for request/response validation
  - `models/` ← Database models
  - `services/` ← Business logic and data handling
  - `static/` ← CSS and JS files for front-end
  - `templates/` ← HTML templates rendered by Jinja2
  - `db/` ← Database configuration and session management
  - `utils/` ← Utility functions (e.g., password hashing)

## Main Responsibilities

1. **App Initialization**
   - `app = FastAPI(...)` initializes the FastAPI application.
   - Version and description are set.

2. **Templates**
   - `Jinja2Templates(directory=...)` configures template rendering.

3. **Static Files**
   - `app.mount('/static', StaticFiles(...))` serves static CSS/JS files.

4. **Routers**
   - `/auth` → `authrouter` for authentication endpoints.
   - `/dashboard` → `dashrouter` for dashboard endpoints.
   - `/doctor` → `doctorrouter` for doctor-related endpoints.
   - `/patient` → `patientrouter` for patient-related endpoints.

5. **Exception Handling**
   - Custom handler for `RequestValidationError` to return meaningful JSON errors.

6. **Root Redirect**
   - `/` redirects to `/auth/login`.

7. **HTML Endpoints**
   - `login.html` → login page.
   - `admin.html` → admin dashboard.
   - `doctor.html` → doctor dashboard.
   - `patient.html` → patient dashboard.
   - `detail.html` → patient details page.

This file acts as the **central hub**, connecting the front-end templates, API routes, and backend logic.
