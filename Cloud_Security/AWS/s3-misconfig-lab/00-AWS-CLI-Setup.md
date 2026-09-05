# AWS CLI Setup Guide for S3 Misconfiguration Lab

## Prerequisites

1. **AWS Account** - You need an active AWS account
2. **Administrator Access** - Or at least S3 full access permissions
3. **Python 3.7+** - For any Python-based components

## Step 1: Install AWS CLI

### Option A: Using pip (Recommended)
```bash
pip install awscli
```

### Option B: Using the bundled installer
Download from: https://awscli.amazonaws.com/AWSCLIV2.msi (Windows)
or https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip (Linux)

### Option C: Using Chocolatey (Windows)
```powershell
choco install awscli
```

### Option D: Using Homebrew (macOS)
```bash
brew install awscli
```

## Step 2: Configure AWS CLI

Run the configuration wizard:
```bash
aws configure
```

You'll be prompted for:
- **AWS Access Key ID** [None]: `YOUR_ACCESS_KEY`
- **AWS Secret Access Key** [None]: `YOUR_SECRET_KEY`
- **Default region name** [None]: `us-east-1` (or your preferred region)
- **Default output format** [None]: `json`

## Step 3: Verify Installation

```bash
aws sts get-caller-identity
```

Should return something like:
```json
{
    "UserId": "AIDACKCEVSQ6CXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/username"
}
```

## Step 4: Create IAM User for Lab (Optional but Recommended)

For better isolation, create a dedicated IAM user:

```bash
# Create IAM user
aws iam create-user --user-name s3-lab-user

# Attach S3FullAccess policy
aws iam attach-user-policy --user-name s3-lab-user --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Create access keys
aws iam create-access-key --user-name s3-lab-user
```

Save the output AccessKeyID and SecretAccessKey, then configure a profile:
```bash
aws configure --profile s3-lab
# Use the credentials from the previous step
```

Then use `--profile s3-lab` with all AWS commands in this lab.

## Step 5: Test Your Setup

```bash
# List S3 buckets (should be empty initially)
aws s3 ls

# If using profile:
aws s3 ls --profile s3-lab
```

## Troubleshooting

### Common Issues:

1. **Access Denied**: Check your IAM permissions
2. **Region Errors**: Ensure you're using the correct region
3. **Expired Credentials**: Refresh your access keys
4. **Proxy Issues**: Configure proxy settings if behind corporate firewall

### Helpful Commands:
```bash
# Check current configuration
aws configure list

# Test credentials
aws sts get-caller-identity

# Get help
aws s3 help
```