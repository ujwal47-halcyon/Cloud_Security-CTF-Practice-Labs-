#!/bin/bash
# S3 Misconfiguration Lab Cleanup Script
# Removes all resources created during the lab

# Load lab configuration if exists
if [ -f "lab-config.txt" ]; then
    echo "📋 Loading lab configuration..."
    source lab-config.txt
else
    echo("❌ No lab configuration found. Nothing to clean up.")
    exit 1
fi

echo "🧹 Cleaning up S3 Misconfiguration Lab Resources"
echo "==============================================="
echo "📍 Region: $REGION"
echo ""

# Function to empty and delete a bucket
cleanup_bucket() {
    local bucket_name=$1
    local bucket_type=$2

    echo "🗑️  Cleaning up $bucket_type bucket: $bucket_name"

    # First, try to delete all objects (including versions if versioning was enabled)
    echo "   Removing all objects..."
    aws s3 rm "s3://$bucket_name" --recursive --force 2>/dev/null || echo "   No objects to remove or access denied"

    # Delete any delete markers (for versioned buckets)
    echo "   Removing delete markers..."
    aws s3api list-object-versions --bucket "$bucket_name" --output json --query 'DeleteMarkers[].{Key:Key,VersionId:VersionId}' 2>/dev/null | \
    jq -c '.[]' 2>/dev/null | while read -r marker; do
        key=$(echo "$marker" | jq -r '.Key')
        version=$(echo "$marker" | jq -r '.VersionId')
        if [ "$key" != "null" ] && [ "$version" != "null" ]; then
            aws s3api delete-object --bucket "$bucket_name" --key "$key" --version-id "$version" 2>/dev/null || true
        fi
    done

    # Delete all object versions
    echo "   Removing all object versions..."
    aws s3api list-object-versions --bucket "$bucket_name" --output json --query 'Versions[].{Key:Key,VersionId:VersionId}' 2>/dev/null | \
    jq -c '.[]' 2>/dev/null | while read -r version; do
        key=$(echo "$version" | jq -r '.Key')
        versionid=$(echo "$version" | jq -r '.VersionId')
        if [ "$key" != "null" ] && [ "$versionid" != "null" ]; then
            aws s3api delete-object --bucket "$bucket_name" --key "$key" --version-id "$versionid" 2>/dev/null || true
        fi
    done

    # Remove bucket policy
    echo "   Removing bucket policy..."
    aws s3api delete-bucket-policy --bucket "$bucket_name" 2>/dev/null || echo "   No policy to remove"

    # Remove public access block
    echo "   Removing public access block..."
    aws s3api delete-public-access-block --bucket "$bucket_name" 2>/dev/null || echo "   No public access block to remove"

    # Remove logging configuration
    echo "   Removing logging configuration..."
    aws s3api put-bucket-logging --bucket "$bucket_name" --bucket-logging-status '{}' 2>/dev/null || echo "   No logging to remove"

    # Remove encryption configuration
    echo "   Removing encryption configuration..."
    aws s3api delete-bucket-encryption --bucket "$bucket_name" 2>/dev/null || echo "   No encryption to remove"

    # Remove versioning
    echo "   Removing versioning configuration..."
    aws s3api put-bucket-versioning --bucket "$bucket_name" --versioning-configuration Status=Suspended 2>/dev/null || echo "   No versioning to remove"

    # Finally, delete the bucket
    echo "   Deleting bucket..."
    if aws s3 rb "s3://$bucket_name" --force 2>/dev/null; then
        echo "   ✅ Bucket deleted successfully"
    else
        echo "   ⚠️  Failed to delete bucket (may have dependencies or access issues)"
    fi

    echo ""
}

echo "Starting cleanup process..."
echo ""

# Clean up each bucket
cleanup_bucket "$PUBLIC_BUCKET" "Public"
cleanup_bucket "$PRIVATE_BUCKET" "Private (misconfigured)"
cleanup_bucket "$LOGGING_BUCKET" "Logging"

# Clean up local files
echo "🧹 Cleaning up local files..."
rm -f lab-config.txt
rm -f "$SENSITIVE_FILE" 2>/dev/null || echo "   No local sensitive file to remove"
rm -f downloaded_*"$SENSITIVE_FILE" 2>/dev/null || echo "   No downloaded sensitive file to remove"

# Remove any other temporary files
rm -f *.txt *.log 2>/dev/null || echo "   No temporary files to clean"

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📝 Summary of what was removed:"
echo "   • Public bucket:    s3://$PUBLIC_BUCKET"
echo "   • Private bucket:   s3://$PRIVATE_BUCKET"
echo "   • Logging bucket:   s3://$LOGGING_BUCKET"
echo "   • Local files:      $SENSITIVE_FILE, lab-config.txt, downloaded_*"
echo ""
echo "💡 Tips for future labs:"
echo "   • Always cleanup AWS resources to avoid unnecessary charges"
echo "   • Consider using AWS CloudFormation or Terraform for repeatable setups"
echo "   • Use AWS Budgets to set alerts on spending"
echo ""
echo "🎓 Lab completion reminder:"
echo "   You've successfully:"
echo "   1. Set up an S3 misconfiguration lab"
echo "   2. Practiced discovering and exploiting public S3 buckets"
echo "   3. Learned how access logging can detect unauthorized access"
echo "   4. Understood remediation steps for S3 security"
echo ""
echo "🔐 Remember: Never leave sensitive data in publicly accessible S3 buckets!"