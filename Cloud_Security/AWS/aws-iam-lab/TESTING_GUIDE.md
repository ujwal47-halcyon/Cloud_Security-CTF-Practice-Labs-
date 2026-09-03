# Testing Guide

## Goal
Walk through the SSRF attack, pull the temporary credentials from the mock metadata service, and use them to list S3 buckets and/or read a secret.

## Prerequisites
- Python 3.7+
- `pip install -r requirements.txt` from the lab directory.
- The lab running (`python app.py`).

## Step 1 – SSRF to IMDSv1
1. Open `http://localhost:5000/`.
2. In the *URL* field, enter:
   ```
   http://169.254.169.254/latest/meta-data/iam/security-credentials/ec2-role
   ```
3. Hit **Load Image**. The page will show the JSON with the fake IAM credentials.

## Step 2 – Obtain a Session Token (IMDSv2)
1. Use curl or a web browser to get a token:
   ```bash
   curl -X PUT http://localhost:5000/latest/api/token
   ```
   Response should be `MOCK-IMDS-TOKEN-ABC`.

## Step 3 – Use the Credentials to list S3 buckets
1. Open the mock console at `http://localhost:5000/admin`.
2. Enter the **Access Key** received in Step 1 in the *auth* box.
3. Type `s3 list-buckets` and press *Run*.
4. You should see the bucket names.

## Step 4 – Pull a secret from Secrets Manager
1. In the same console, type `secrets get`.
2. The output will be the secret value for `DB_PASSWORD`.

## What you learned
- SSRF can steal credentials if IMDS is exposed.
- IMDSv2 helps mitigate SSRF by requiring a session token.
- Weak IAM policies can give attackers access to S3/Secrets.
