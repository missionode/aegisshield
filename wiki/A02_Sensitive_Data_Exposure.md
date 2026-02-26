# OWASP Top 10: Sensitive Data Exposure (A02:2021)
Sensitive Data Exposure occurs when an application doesn't adequately protect sensitive information such as financial data, health records, or PII.

### 🛡️ Common Vulnerabilities:
- Storing secrets in clear text (e.g., `.env` files).
- Weak file permissions.
- Insecure storage of database credentials.

### 🛠️ AegisShield Prevention:
- Automatically harden file permissions for `.env` files.
- Monitor for exposed credentials in the production root.
