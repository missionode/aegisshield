# Product Definition: Plant Doctor

## Vision
Plant Doctor is an AI-powered web application that helps gardening enthusiasts diagnose plant diseases, receive care reminders, and get expert advice to ensure their plants thrive.

## Core Features

1.  **User Accounts**
    -   Secure Login and Signup.
    -   User Profile management (Name, Location, Avatar).
    -   Personalized "My Garden" dashboard.

2.  **Plant Diagnosis (AI Scanner)**
    -   Camera interface to capture plant photos.
    -   "Analysis" animation and processing state.
    -   Instant diagnosis results (Disease Name, Confidence Level).
    -   Actionable advice: "Immediate Action" vs. "Long Term Care".
    -   Product recommendations for treatment.

3.  **Dashboard & History**
    -   View recent scans and diagnosis history.
    -   "My Garden" section for saved plants.
    -   Weather/Status summary (Mockup).

4.  **Onboarding**
    -   Educational carousel for new users explaining the "Snap -> Diagnose -> Heal" workflow.

## User Flow
1.  **Landing:** User arrives at `index.html`.
2.  **Auth:** User logs in or signs up.
3.  **Onboarding:** New users see the how-to carousel.
4.  **Dashboard:** User sees their dashboard.
5.  **Scan:** User clicks "Scan Plant", takes/uploads a photo.
6.  **Analysis:** System processes the image.
7.  **Result:** User views the diagnosis and care plan.
8.  **Save:** User saves the result to "My Garden".

## Tech Stack (Planned)
-   **Backend:** Python Django
-   **Database:** SQLite (dev) / PostgreSQL (prod)
-   **Frontend:** Django Templates (HTML/Tailwind CSS from Prototype)
-   **Styling:** Tailwind CSS (via CDN or local build)
