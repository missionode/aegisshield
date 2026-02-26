# OWASP Top 10: Insecure Design (A04:2021)
Insecure design is a broad category representing different weaknesses, where "design" is the focus, rather than "implementation." It involves logic flaws where the application's business logic can be abused.

### 🛡️ Common Logic Flaws:
- **Insecure Direct Object Reference (IDOR):** Accessing resources by guessing IDs (e.g., `?id=101`).
- **Missing Function Level Access Control:** Regular users accessing admin endpoints.
- **Race Conditions:** Exploiting the timing of multi-threaded operations.

### 🛠️ AegisShield Prevention & Code Standards:
- **Rule:** Never trust user input for database primary keys.
- **Rule:** Implement centralized authorization decorators for all endpoints.
- **Scan Pattern:** Search for missing `@login_required` or equivalent decorators.
