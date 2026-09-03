# AWS IAM Privilege Escalation CTF Lab

Welcome to your first AWS IAM Cloud Security CTF Lab! This is an intentionally vulnerable web application running locally that simulates a real-world cloud attack path.

## Lab Scenario
You are a penetration tester hired to audit a car dealership website running on an AWS EC2 instance. The application has an image proxy feature. Your objective is to:
1. Exploit the Server-Side Request Forgery (SSRF) vulnerability.
2. Query the Instance Metadata Service (IMDS) to compromise the IAM role attached to the EC2 instance.
3. Access S3 and Secrets Manager to find the "flag" (DB password).

## Quick Start

```bash
cd aws-iam-lab
pip install -r requirements.txt
python app.py
```

- Public Web Application: `http://localhost:5000/`
- Mock AWS CLI Console: `http://localhost:5000/admin`
