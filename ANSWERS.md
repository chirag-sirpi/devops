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
