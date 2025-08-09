# AWS Inspector Code Security Demo

This repository demonstrates AWS Inspector Code Security capabilities by providing a vulnerable Python Flask application and Terraform infrastructure for testing security scanning features.

## Overview

AWS Inspector Code Security scans your application source code, dependencies, and infrastructure as code (IaC) for software vulnerabilities and misconfigurations. This demo includes intentionally vulnerable code to showcase the scanning capabilities.

![AWS Inspector Code Security Overview](images/inspector-overview.png)

## Project Structure

```
├── app/                    # Vulnerable Python Flask application
│   ├── main.py            # Flask app with XSS, Command Injection, and LDAP Injection
│   ├── requirements.txt   # Python dependencies
│   └── .env.example      # Environment variables template
├── iaac/                  # Terraform infrastructure code
│   ├── main.tf           # S3 bucket with security misconfigurations
│   └── variables.tf      # Terraform variables
└── images/               # Screenshots and documentation images
```

## Vulnerabilities Included

### Application Vulnerabilities (app/main.py)

1. **Cross-Site Scripting (XSS)**
   - Unescaped user input in HTML templates
   - Test payload: `<script>alert('XSS')</script>`

2. **Command Injection**
   - Direct shell command execution with user input
   - Test payload: `localhost; whoami`

3. **LDAP Injection**
   - Unsanitized LDAP filter construction
   - Test payload: `admin)(&(objectClass=*`

### Infrastructure Vulnerabilities (iaac/main.tf)

1. **Public S3 Bucket**
   - Unrestricted public read access
   - No encryption at rest
   - Versioning disabled
   - Inadequate logging configuration

## AWS Inspector Setup

### Step 1: Create Configuration

![Create Configuration](images/create-configuration.png)

1. Navigate to AWS Inspector in the AWS Console
2. Go to Code Security section
3. Create a new scan configuration
4. Enable SAST, Secrets, and SCA scanning
5. Configure scan frequency (Weekly recommended)

### Step 2: Connect Repository

![Code Repositories](images/code-repositories.png)

1. Connect your code repository to Inspector
2. Configure scan settings and triggers
3. Set up integration with your SCM platform

### Step 3: Review Results

![Inspector Dashboard](images/inspector-dashboard.png)

Inspector will scan and identify:
- Security vulnerabilities in application code
- Hardcoded secrets and credentials
- Infrastructure misconfigurations
- Dependency vulnerabilities

## Running the Demo

### Prerequisites

- Python 3.8+
- Flask
- Terraform (for infrastructure deployment)
- AWS CLI configured

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd aws-inspector-code-scan-demo
```

2. Set up Python environment:
```bash
cd app
pip install -r requirements.txt
```


4. Run the vulnerable application:
```bash
python main.py
```

5. Access the application at `http://localhost:5000`

### Testing Vulnerabilities

#### XSS Testing
1. Navigate to the search form
2. Enter: `<script>alert('XSS')</script>`
3. Submit to see the script execute

#### Command Injection Testing
1. Navigate to the ping form
2. Enter: `localhost; whoami`
3. Submit to see command execution

#### LDAP Injection Testing
1. Navigate to the LDAP search form
2. Enter: `admin)(&(objectClass=*`
3. Submit to see filter manipulation

### Infrastructure Deployment

1. Navigate to infrastructure directory:
```bash
cd iaac
```

2. Initialize and deploy:
```bash
terraform init
terraform plan
terraform apply
```

## Security Remediation

This code is intentionally vulnerable for demonstration purposes. In production:

1. **Sanitize all user inputs**
2. **Use parameterized queries**
3. **Implement proper output encoding**
4. **Use environment variables for secrets**
5. **Enable S3 encryption and proper access controls**
6. **Implement proper logging and monitoring**

## AWS Inspector Integration

AWS Inspector Code Security will automatically detect:

- **High-severity vulnerabilities** in the application code
- **Infrastructure misconfigurations** in Terraform files
- **Dependency vulnerabilities** in requirements.txt
- **Security best practice violations**

## Disclaimer

⚠️ **WARNING**: This application contains intentional security vulnerabilities and should NEVER be deployed in a production environment. Use only for educational and testing purposes in isolated environments.

## License

This project is for educational purposes only.