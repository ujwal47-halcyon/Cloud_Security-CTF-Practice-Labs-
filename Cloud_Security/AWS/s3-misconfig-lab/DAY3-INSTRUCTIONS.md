# Day 3: S3 Bucket Misconfigurations Lab

## 🎯 Learning Objectives
By the end of this lab, you will be able to:
1. Identify common S3 bucket misconfigurations that lead to data exposure
2. Use AWS CLI to discover publicly accessible S3 buckets without credentials
3. Exploit misconfigurations to access sensitive data (in a controlled, legal environment)
4. Implement remediation steps to secure S3 buckets
5. Understand how access logging can detect unauthorized access attempts

## ⏱️ Estimated Time: 45-60 minutes

## 📋 Prerequisites
- AWS CLI installed and configured (see 00-AWS-CLI-Setup.md)
- Active AWS account with S3 permissions
- Basic understanding of S3 concepts (buckets, objects, permissions)

## 🚀 Lab Execution Steps

### Step 1: Environment Setup (5 minutes)
```bash
# Navigate to lab directory
cd "C:\Users\Ujwal\Downloads\aws testing\s3-misconfig-lab"

# Review AWS CLI setup if needed
# cat 00-AWS-CLI-Setup.md

# Create the lab environment
./01-Setup-Lab.sh
```

**What happens during setup:**
- 3 unique S3 buckets are created (public, private, logging)
- A fake sensitive file (`passwords.txt`) is uploaded to the "private" bucket
- The private bucket is intentionally made publicly accessible via bucket policy
- Access logging is enabled on both buckets
- Configuration is saved to `lab-config.txt`

### Step 2: Exploitation Practice (20-25 minutes)
```bash
# Run the exploitation demonstration
./02-Exploit-Lab.sh
```

**Key learning moments:**
1. **Discovery Phase**: Learn how to test bucket accessibility without credentials using `--no-sign-request`
2. **Exploitation Phase**: Discover how to access the misconfigured bucket and download sensitive data
3. **Investigation Phase**: Check access logs to see if your activity was recorded
4. **Remediation Phase**: Learn how to fix the misconfiguration

**What you'll see:**
- How the "private" bucket (meant to be secure) is actually accessible to anyone
- How to download the leaked `passwords.txt` file containing fake credentials
- What an attacker could do with AWS keys, database passwords, and API keys
- How access logging captures your access attempts (blue team perspective)

### Step 3: Reflection and Discussion (10-15 minutes)
After running the exploitation script, consider these questions:

** Offensive Security Thinking:**
1. How would an attacker discover this bucket in the wild?
2. What automated tools exist for scanning public S3 buckets?
3. What other types of sensitive data might be exposed in misconfigured buckets?
4. How could you chain this access with other AWS services?

** Defensive Security Thinking:**
1. How could this misconfiguration have been prevented?
2. What AWS native tools could detect this misconfiguration?
3. How would you respond if you discovered this in your environment?
4. What monitoring and alerting would you set up?

### Step 4: Cleanup (5 minutes)
```bash
# CRITICAL: Always cleanup to avoid AWS charges!
./03-Cleanup-Lab.sh
```

**Verify cleanup worked:**
```bash
# Should show no buckets matching our lab pattern
aws s3 ls | grep $(cat lab-config.txt 2>/dev/null | grep LAB_NAME | cut -d= -f2) || echo "No lab buckets found - cleanup successful!"
```

## 🔍 Key Concepts Covered

### S3 Misconfiguration Types Demonstrated:
1. **Overly Permissive Bucket Policies**: Granting `s3:GetObject` to `*` (everyone)
2. **Missing Block Public Access Settings**: Not enabling S3's built-in protections
3. **Lack of Least Privilege**: Giving more permissions than necessary
4. **Insufficient Monitoring**: Although we enabled logging, real-world cases often lack this

### AWS Security Features Practiced:
- `--no-sign-request`: Accessing public resources without AWS credentials
- Bucket policies: Understanding how they override IAM permissions
- Access logging: Tracking who accessed what and when
- Block Public Account: The setting that should prevent this issue

### Real-World Attack Vectors Simulated:
1. **Credentials Exposure**: AWS keys leading to full account compromise
2. **Data Breach**: Database passwords and internal credentials exposed
3. **Financial Fraud**: API keys used for unauthorized transactions
4. **Privilege Escalation**: Using exposed credentials to access other AWS services

## 🛡️ Remediation Checklist
After this lab, you should be able to implement these fixes:

✅ **Immediate Actions:**
- Remove public bucket policies granting access to `*`
- Enable S3 Block Public Access settings
- Review and tighten IAM policies

✅ **Detective Controls:**
- Enable access logging on all S3 buckets
- Set up CloudWatch alerts for unusual access patterns
- Use AWS Config rules to detect public buckets
- Enable AWS Security Hub findings

✅ **Preventative Controls:**
- Implement least privilege access principles
- Use bucket policies that explicitly deny public access
- Encrypt sensitive data at rest (SSE-S3, SSE-KMS, or client-side)
- Enable versioning and MFA Delete for critical buckets
- Regularly audit permissions with AWS IAM Access Analyzer

## 📝 Documentation for Your Report
When documenting your findings (for bug bounty or internal reporting):

**Title:** 
`S3 Bucket Misconfiguration Leading to Unauthorized Access to Sensitive Data`

**Description:**
"During testing, discovered an S3 bucket intentionally configured with public read access containing sensitive credentials including AWS access keys, database passwords, and API keys. The bucket policy granted `s3:GetObject` and `s3:ListBucket` permissions to principal `*` (anyone on the internet)."

**Steps to Reproduce:**
1. Identify target S3 bucket (in our case: `{PRIVATE_BUCKET}`)
2. Run: `aws s3 ls s3://{BUCKET_NAME} --no-sign-request`
3. List contents: `aws s3 ls s3://{BUCKET_NAME}/ --no-sign-request --recursive`
4. Download sensitive file: `aws s3 cp s3://{BUCKET_NAME}/sensitive-file.txt . --no-sign-request`

**Impact:**
- Full AWS account compromise possible with exposed keys
- Database breach with exposed credentials
- Financial loss from abused API keys
- Reputational damage from data exposure

**Remediation:**
1. Remove public access from bucket policy
2. Enable S3 Block Public Access
3. Rotate any exposed credentials immediately
4. Review CloudTrail logs for unauthorized access
5. Implement regular S3 security audits

## 🧪 Variations to Try (If Time Permits)
1. **Different Misconfigurations**: Try setting up a bucket with public ACL instead of policy
2. **Regional Variations**: Create buckets in different AWS regions
3. **Encryption Testing**: Add SSE-S3 or SSE-KMS encryption to see if it helps
4. **Logging Evasion**: Test if access logging captures `--no-sign-request` access (it does!)
5. **Cross-Account Access**: Experiment with bucket policies granting access to specific AWS accounts

## 🎓 Completion Criteria
You've completed the lab when you can:
- [ ] Explain how the misconfiguration occurred
- [ ] Demonstrate accessing the bucket without credentials
- [ ] Show how to download the sensitive file
- [ ] Describe what an attacker could do with the exposed data
- [ ] Explain how to fix the misconfiguration
- [ ] Describe how access logging helps detect this issue
- [ ] Successfully clean up all lab resources

## ⚠️ Important Reminders
1. **ALWAYS cleanup** - Run `./03-Cleanup-Lab.sh` when finished
2. **Use fake data only** - The lab uses deliberately fake credentials
3. **Never point this at real AWS resources** - This is for educational purposes only
4. **Report real findings responsibly** - If you find actual misconfigurations in the wild, follow responsible disclosure practices
5. **Stay within legal boundaries** - Only test systems you own or have explicit permission to test

## 📚 Further Learning
After this lab, explore:
- AWS S3 Security Best Practices documentation
- AWS Macie for automated sensitive data discovery
- AWS Config rules for S3 (e.g., `s3-bucket-public-read-prohibited`)
- Amazon S3 Access Points for more granular access control
- AWS Well-Architected Framework Security Pillar
- S3 Batch Operations for large-scale remediation

---
**Lab Complete!** You now have hands-on experience with one of the most common cloud security misconfigurations. Remember: the goal is to learn how to both identify and prevent these issues in real environments.