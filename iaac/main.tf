terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# Vulnerable: S3 bucket with public access
resource "aws_s3_bucket" "vulnerable_bucket" {
  bucket = var.bucket_name
}

# Vulnerable: Public read access
resource "aws_s3_bucket_public_access_block" "vulnerable_bucket_pab" {
  bucket = aws_s3_bucket.vulnerable_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# Vulnerable: Public read policy
resource "aws_s3_bucket_policy" "vulnerable_bucket_policy" {
  bucket = aws_s3_bucket.vulnerable_bucket.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.vulnerable_bucket.arn}/*"
      }
    ]
  })
}

# Vulnerable: No encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "vulnerable_bucket_encryption" {
  bucket = aws_s3_bucket.vulnerable_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Vulnerable: No versioning
resource "aws_s3_bucket_versioning" "vulnerable_bucket_versioning" {
  bucket = aws_s3_bucket.vulnerable_bucket.id
  versioning_configuration {
    status = "Disabled"
  }
}

# Vulnerable: No logging
resource "aws_s3_bucket_logging" "vulnerable_bucket_logging" {
  bucket = aws_s3_bucket.vulnerable_bucket.id

  target_bucket = aws_s3_bucket.vulnerable_bucket.id
  target_prefix = "log/"
}