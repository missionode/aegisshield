# Attack Type: Directory Traversal (LFI/RFI)
Directory traversal (also known as file path traversal) is a web security vulnerability that allows an attacker to read arbitrary files on the server that is running an application.

### 🛡️ Common Vulnerabilities:
- Input parameters like `?file=...` are not sanitized.
- Accessing `../../etc/passwd` or sensitive configuration files.

### 🛠️ AegisShield Prevention:
- Monitor hits for `..` patterns in paths.
- Harden root directories against world-writable bits.
