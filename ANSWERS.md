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

---

## Secret Mission: Custom Semgrep Rule

### Question: What pattern syntax did your custom rule use to match os.system() calls, and why is this approach better than a regex?
**Answer:**
In this project extension, I used `os.system(...)` to match the pattern because Semgrep parses the code's Abstract Syntax Tree (AST) to match the call structurally. This is better than a regex because it is resilient to variations in whitespace, single/double quotes, variable names, and multi-line formatting, preventing false positives and negatives.

### Question: Which 4 security jobs ran in your pipeline, and what does each one scan for?
**Answer:**
The 4 jobs are:
1. **Secrets Detection (Gitleaks)**: Scans Git commits and history for hardcoded secrets, keys, or access tokens.
2. **SAST (Semgrep)**: Scans the application source code for patterns indicating software security vulnerabilities like SQL Injection, custom code anti-patterns, or bad practices.
3. **Dependency Scan (Trivy FS)**: Scans project package manifests (such as `requirements.txt`) for known vulnerabilities (CVEs) in third-party libraries.
4. **Container Image Scan (Trivy Image)**: Scans the compiled container image filesystem and its base OS libraries for operating system and application dependency vulnerabilities.

### Question: Thanks for doing this project!
**Answer:**
I did this project today to learn how to design, implement, and run a multi-stage security pipeline using GitHub Actions and remediate real code, dependency, and container vulnerabilities. Another skill I want to learn is dynamic application security testing (DAST) using OWASP ZAP in a Kubernetes environment.

### Question: How long did it take you to complete this project?
**Answer:**
This project took me approximately 1 hour to complete. The most challenging part was purging the local Git repository history to ensure Gitleaks was satisfied after fixing the hardcoded credentials, and configuring custom Semgrep rules to detect in-memory SQLite connections.

### Question: What were the key tools and concepts you learnt in this project?
**Answer:**
The key tools I used include Gitleaks, Semgrep, Trivy, and GitHub Actions. Key concepts I learnt include static application security testing (SAST), software composition analysis (SCA), secrets detection and lifecycle remediation, container image security hardening using Alpine base images, and running non-root container contexts.
