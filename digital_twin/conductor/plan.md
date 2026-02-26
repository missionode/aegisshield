# Master Implementation Plan: Plant Doctor (Django)

## Phase 1: Project Foundation ✅
**Goal:** Initialize the Django project and set up the base infrastructure.

- [x] **Initialize Django Project**
    - Create virtual environment.
    - Install `django` and `django-tailwind`.
    - Start project `plant_doctor`.
- [x] **App Structure**
    - Create apps: `core`, `users`, `diagnose`.
- [x] **Static & Templates Setup**
    - Configure `STATICFILES_DIRS` and `TEMPLATES`.
    - Move Prototype HTML files to `templates/` folder.
    - Create a `base.html` template.

## Phase 2: Authentication & User Management ✅
**Goal:** Allow users to sign up, log in, and manage their profiles.

- [x] **User Model**
    - Extend `AbstractUser` in `users/models.py`.
    - Add fields: `full_name`, `location`, `avatar`.
- [x] **Auth Views**
    - Implement Login View.
    - Implement Signup View.
    - Implement Logout.
- [x] **Profile View**
    - Implement Profile management.
- [x] **Onboarding**
    - specific view for `onboarding.html` shown after first signup.

## Phase 3: Core Logic (Scanner & Diagnosis) ✅
**Goal:** Implement the scanning workflow and display results.

- [x] **Data Models**
    - `Disease`: Name, Description, Immediate Action, Long Term Care, Recommended Products.
    - `Scan`: ForeignKey to User, ImageField, Date, Result, Confidence Score.
- [x] **Scanner View**
    - Render `scanner.html`.
    - Handle file upload.
- [x] **Analysis Logic**
    - **Integrate AI Vision API:** Integrated Google Gemini API (`gemini-flash-latest`).
    - **Prompt Engineering:** Structured JSON response for diagnosis and care plans.
    - **Handling:** Parse the AI response and save it to the `Scan` model.
- [x] **Result View**
    - Render `result.html` with dynamic data.

## Phase 4: Dashboard & History ✅
**Goal:** Tie everything together in the user dashboard.

- [x] **Dashboard View**
    - Render `dashboard.html`.
    - Fetch and display the user's `Scan` history.
    - "My Garden" section: Show saved/favorited scans.
- [x] **History View**
    - Integrated into the Dashboard with pagination.
- [x] **Navigation**
    - All links updated to use Django URL names.

## Phase 5: Refinement ✅
**Goal:** Polish the UI and ensure smooth UX.

- [x] **Template Inheritance**
    - Refactored HTML files to extend `base.html`.
- [x] **Error Handling**
    - Fixed 404 on `/accounts/login/` by configuring `LOGIN_URL`.
    - Improved AI error handling to display specific API errors.
- [x] **Admin Panel**
    - Configured for `User`, `Disease`, and `Scan`.

## Phase 6: Final Review ✅
- [x] Verify flow: Landing -> Signup -> Onboarding -> Dashboard -> Scan -> Result.
- [x] Check responsiveness (Mobile/Desktop).