# Secure Coding Standard: Input Validation & Injection
Injection vulnerabilities (A03:2021) occur when untrusted data is sent to an interpreter as part of a command or query.

### 🛡️ Dangerous Logic Patterns:
- **`eval()` and `exec()`:** These allow execution of arbitrary strings as code.
- **`os.system()` / `subprocess.Popen(shell=True)`:** High risk of command injection.
- **Raw SQL Queries:** String concatenation in database queries leads to SQLi.

### 🛠️ AegisShield Code Standards:
- **Standard:** Use Parameterized Queries (Prepared Statements) for all DB access.
- **Standard:** Use `subprocess.run(shell=False)` with a list of arguments.
- **Standard:** Replace `eval()` with safe alternatives like `json.loads()`.

### 🔍 AI Scan Trigger:
AegisShield will flag any instance of `eval`, `exec`, or `shell=True` as a **LOGIC_RISK**.
