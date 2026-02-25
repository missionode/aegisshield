# Specification: Implement Expert Entry and Domain Diagnosis Engine

## Overview
This track focuses on building the initial "Expert Entry" phase of AegisShield. It includes the landing page (Home) where users can input a domain for an "Instant Diagnosis." The AI engine will perform a remote profile scan (SSL, Headers, Port analysis) and provide an Instant Health Score.

## User Stories
- **As a user**, I want to enter my domain name on the home page so I can see its current security posture.
- **As a user**, I want to receive an instant security rating (0-100) based on a non-invasive remote scan.
- **As a user**, I want to see a high-level breakdown of my domain's external footprint (SSL status, security headers).

## Functional Requirements
- **Domain Input:** A centralized, neon-styled input field on the home page.
- **Remote Scanner:** A background worker (FastAPI) that performs:
    - SSL/TLS certificate verification.
    - Security Header analysis (HSTS, CSP, X-Frame-Options, etc.).
    - Common Port scanning (non-intrusive).
- **Health Score Algorithm:** A weighted logic that converts scan results into a 0-100 score.
- **Diagnosis HUD:** A Reflex-powered view displaying the score and scan summary with "Cyber-Premium" aesthetics.

## Technical Constraints
- Must be implemented using **Reflex** for the UI.
- Scans must be performed asynchronously via **FastAPI** to prevent UI blocking.
- Styling must strictly follow the **Design System** (Deep Space background, Electric Cyan/Neon Magenta accents).

## Success Criteria
- A user can enter a domain and receive a score within 10 seconds.
- The UI reflects the "Expertise" voice—precise and calm.
- Scan results are accurately displayed in the Diagnosis HUD.
