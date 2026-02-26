# OWASP Top 10: Broken Access Control (A01:2021)
Access control enforces policy such that users cannot act outside of their intended permissions. Failures typically lead to unauthorized information disclosure, modification, or destruction of all data or performing a business function outside the user's limits.

### 🛡️ Common Vulnerabilities:
- Violation of the principle of least privilege.
- Bypassing access control checks by modifying the URL (parameter tampering).
- Permitting viewing or editing someone else's account.

### 🛠️ AegisShield Prevention:
- Ensure `.env` and `.git` files are protected (permissions 600).
- Monitor `/admin` and sensitive paths for unauthorized probes.
