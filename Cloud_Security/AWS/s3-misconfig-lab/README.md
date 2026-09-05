# S3 Bucket Misconfigurations Lab

## 🎯 Lab Objective
Learn how to discover, exploit, and remediate S3 bucket misconfigurations that lead to unauthorized access to sensitive data.

## ⚠️ Important Safety Notes
- This lab creates REAL AWS resources in your account
- Always run the cleanup script when finished to avoid charges
- Never use real credentials or sensitive data in this lab
- The lab uses fake credentials for educational purposes only

## 📁 Lab Structure
```
s3-misconfig-lab/
├── 00-AWS-CLI-Setup.md     # AWS CLI setup instructions
├── 01-Setup-Lab.sh         # Creates the lab environment
├── 02-Exploit-Lab.sh       # Demonstrates exploitation techniques
├── 03-Cleanup-Lab.sh       # Removes all lab resources
├── lab-config.txt          # Generated during setup (do not edit)
└── README.md               # This file
```

## 🧪 Lab Overview
This lab simulates a real-world scenario where a developer accidentally makes backups public:
- **3 buckets created**: public, private (intentionally misconfigured), and logging
- **Fake sensitive file**: `passwords.txt` containing mock AWS keys, passwords, and API keys
- **Intentional misconfiguration**: Private bucket made publicly accessible via bucket policy
- **Access logging**: Enabled to show how unauthorized access can be detected

## 🚀 How to Run the Lab

### Prerequisites
1. AWS CLI installed and configured (see `00-AWS-CLI-Setup.md`)
2. AWS account with S3 permissions
3. Bash shell (Windows users can use Git Bash or WSL)

### Step-by-Step Instructions

#### 1. Setup the Lab Environment
```bash
cd "C:\Users\Ujwal\Downloads\aws testing\s3-misconfig-lab"
./01-Setup-Lab.sh
```

This will:
- Create 3 S3 buckets with unique names
- Upload a fake sensitive file (`passwords.txt`)
- Intentionally misconfigure the private bucket to be publicly accessible
- Enable access logging on both buckets
- Save configuration to `lab-config.txt`

#### 2. Practice Exploitation
```bash
./02-Exploit-Lab.sh
```

This will demonstrate:
- How to access buckets without AWS credentials (using `--no-sign-request`)
- How to discover the misconfigured bucket containing sensitive data
- How to download the leaked sensitive file
- How to check access logs to see if the access was recorded
- What an attacker could do with the leaked information

#### 3. Learn Remediation
The exploitation script shows how to fix the misconfiguration:
- Remove public bucket policies
- Enable S3 Block Public Access
- Verify the fix works
- Additional security best practices

#### 4. Cleanup (IMPORTANT)
```bash
./03-Cleanup-Lab.sh
```

This will:
- Remove all objects from the buckets
- Delete all three buckets
- Clean up local temporary files
- Prevent ongoing AWS charges

## 🔍 What You'll Learn

### Offensive Security Perspective
- How attackers discover publicly accessible S3 buckets
- Common misconfiguration patterns (bucket policies, ACLs)
- How to access S3 resources without credentials using `--no-sign-request`
- What types of sensitive data are commonly exposed
- How access logging can be used for detection

### Defensive Security Perspective
- How S3 bucket misconfigurations occur in real environments
- The importance of least privilege access controls
- How to detect unauthorized S3 access through logging
- Best practices for securing S3 buckets:
  - Block Public Access settings
  - Proper bucket policies
  - Encryption at rest
  - Versioning and backups
  - Regular security audits

### Key AWS CLI Commands Practiced
```bash
# Basic bucket operations
aws s3 ls
aws s3 mb s3://bucket-name
aws s3 rb s3://bucket-name --force

# Object operations
aws s3 cp local-file s3://bucket/
aws s3 cp s3://bucket/file .
aws s3 ls s3://bucket/
aws s3 rm s3://bucket/file

# Bucket policy and configuration
aws s3api put-bucket-policy
aws s3api get-bucket-policy
aws s3api delete-bucket-policy
aws s3api put-public-access-block
aws s3api get-bucket-logging
aws s3api put-bucket-logging

# Testing without credentials
aws s3 ls s3://bucket --no-sign-request
aws s3 cp s3://bucket/file . --no-sign-request
```

## 📋 Lab Variables
The lab generates unique bucket names using a timestamp to avoid conflicts:
- `PUBLIC_BUCKET`: `{lab-prefix}-public`
- `PRIVATE_BUCKET`: `{lab-prefix}-private` (intentionally made public)
- `LOGGING_BUCKET`: `{lab-prefix}-logging`
- `REGION`: us-east-1 (configurable in the setup script)
- `SENSITIVE_FILE`: passwords.txt

## 🛡️ Real-World Relevance
This lab mirrors actual incidents where:
- Companies accidentally exposed AWS keys in public S3 buckets
- Customer data was leaked due to misconfigured bucket policies
- Internal source code and configuration files were made publicly accessible
- Attackers used automated tools to scan for and exploit public S3 buckets

## 🧹 Troubleshooting

### "Access Denied" Errors
1. Verify your AWS credentials are correct: `aws sts get-caller-identity`
2. Ensure your user has S3 permissions: `AmazonS3FullAccess` or equivalent
3. Check that you're in the correct AWS region

### Bucket Already Exists
The lab uses timestamp-based names to prevent conflicts, but if you run into naming issues:
- Delete any existing buckets with similar names manually
- Or modify the `LAB_NAME` variable in `01-Setup-Lab.sh`

### Cleanup Issues
If cleanup fails:
1. Wait a few minutes and try again (eventual consistency)
2. Check if there are object locks or legal holds
3. Manually delete objects via AWS Console if needed
4. Run cleanup script again

## 🎓 Next Steps
After completing this lab, consider:
1. Setting up AWS Config rules to detect public buckets
2. Creating CloudWatch alerts for S3 access patterns
3. Practicing with other AWS services (IAM, EC2, RDS) misconfigurations
4. Learning about AWS Macie for automated sensitive data discovery
5. Participating in AWS Security specializations or certifications

## 📚 References
- AWS S3 Security Best Practices: https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
- Block Public Access: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
- S3 Access Logging: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access_logging.html
- AWS Security Hub: https://aws.amazon.com/security-hub/
- Amazon Macie: https://aws.amazon.com/macie/

---
**Remember**: Always cleanup your lab resources to avoid unexpected AWS charges!
Run `./03-Cleanup-Lab.sh` when you're finished.