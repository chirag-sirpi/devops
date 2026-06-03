# Project Questions and Answers

## Step 0: Before We Start

### Question: What are we doing in this project?
**Answer:**
In this project, I'm building a complete multi-stage security pipeline using GitHub Actions with open-source tools (Gitleaks, Semgrep, Trivy) applied to a deliberately vulnerable Python Flask application so that I can automatically catch secrets leaks, code vulnerabilities, insecure package dependencies, and container misconfigurations on every push, and learn how to remediate them.

---

## Step 1: Create the Vulnerable Flask Application

### Question: What are we doing in this step?
**Answer:**
In this step, I'm creating a deliberately vulnerable Flask application, custom dependency requirements, and a Dockerfile with security misconfigurations so that the pipeline can detect and catch these specific security flaws.

### Question: What are the four types of security vulnerabilities you intentionally introduced across these three files?
**Answer:**
The four vulnerability types are:
1. **Hardcoded Secrets/Credentials**: AWS access credentials and Slack Bot Token in `app.py`.
2. **SQL Injection**: Dynamic string formatting query execution in SQLite inside `app.py`.
3. **Vulnerable Dependencies**: Outdated package versions (`Flask==2.0.0`, `requests==2.20.0`, `urllib3==1.24.2`) in `requirements.txt`.
4. **Container Misconfigurations**: Running as `root` (lack of USER specification) and using an outdated base image (`python:3.9-slim-buster`) in `Dockerfile`.

---

## Step 2: Build the Security Pipeline

### Question: What are we doing in this step?
**Answer:**
In this step, I'm building a GitHub Actions CI/CD workflow with 4 parallel security scanning jobs (Gitleaks, Semgrep, Trivy FS, and Trivy Image) so that I can automatically scan the codebase and container images for secrets, code vulnerabilities, library dependencies, and container configuration issues on every push.

### Question: Why are all 4 pipeline jobs failing?
**Answer:**
The jobs are failing because the app contains:
1. **Secrets Detection (Gitleaks)**: Flags hardcoded AWS credentials and database passwords in `app.py`.
2. **SAST (Semgrep)**: Flags a SQL injection vulnerability, insecure host binding, and an SQLite in-memory database connection in `app.py`, as well as the container running as root in `Dockerfile`.
3. **Dependency Scan (Trivy FS)**: Flags outdated Python packages (`Flask==2.0.0`, `requests==2.20.0`, `urllib3==1.24.2`) containing known high/critical CVEs in `requirements.txt`.
4. **Container Image Scan (Trivy Image)**: Flags multiple system package vulnerabilities in the old `python:3.9-slim-buster` base image in `Dockerfile`.


---

## Step 3: Remediate the Vulnerabilities

### Question: What are we doing in this step?
**Answer:**
In this step, I'm fixing each category of security issues in the Flask app (secrets, SQL injection, outdated packages, container config) so that the pipeline can run against a secure codebase and verify the remediation.

### Question: How did you fix the SQL injection vulnerability in app.py?
**Answer:**
I replaced the f-string query with a parameterized SQL query: `SELECT * FROM users WHERE name = ?` and passed the user input as a query parameter tuple `(username,)`. The `?` placeholder ensures that SQLite treats user inputs strictly as data values rather than executable SQL code, eliminating the SQL injection risk.

### Question: What were the four vulnerability categories you fixed, and how did you fix each one?
**Answer:**
I fixed secrets by moving them to environment variables loaded via `os.getenv`. SQL injection by using query parameterization (the `?` placeholder in SQLite). dependencies by upgrading packages to secure versions (`Flask>=3.0.3`, `requests>=2.32.2`, `urllib3>=2.2.1`) in `requirements.txt`. and the container by switching the base image to `python:3.12-alpine` and running under a non-root user (`appuser`).

---

## Step 4: Verify the Hardened Pipeline

### Question: What are we doing in this step?
**Answer:**
In this step, I'm pushing the remediated code to GitHub so that I can confirm that all 4 security scanning jobs in the workflow pass successfully (turn green).
