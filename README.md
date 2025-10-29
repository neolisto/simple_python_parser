# Simple Python Parser!

<!-- Replace neolisto_simple_python_parser and neolisto with your actual SonarCloud/SonarQube values -->

## SonarQube/SonarCloud Badges

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=neolisto_simple_python_parser&metric=alert_status)](https://sonarcloud.io/dashboard?id=neolisto_simple_python_parser)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=neolisto_simple_python_parser&metric=coverage)](https://sonarcloud.io/dashboard?id=neolisto_simple_python_parser)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=neolisto_simple_python_parser&metric=bugs)](https://sonarcloud.io/dashboard?id=neolisto_simple_python_parser)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=neolisto_simple_python_parser&metric=vulnerabilities)](https://sonarcloud.io/dashboard?id=neolisto_simple_python_parser)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=neolisto_simple_python_parser&metric=code_smells)](https://sonarcloud.io/dashboard?id=neolisto_simple_python_parser)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=neolisto_simple_python_parser&metric=security_rating)](https://sonarcloud.io/dashboard?id=neolisto_simple_python_parser)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=neolisto_simple_python_parser&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=neolisto_simple_python_parser)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=neolisto_simple_python_parser&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=neolisto_simple_python_parser)

## Description

Azure Function App for parsing web site with the Python code.

## Setup Instructions

### Prerequisites
- Python 3.x
- Azure Functions Core Tools
- Azure CLI (for deployment)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run locally:
```bash
func start
```

### Deployment

Deploy to Azure using the provided script:
```bash
./deploy_function_app.sh
```

## Configuration for SonarQube Analysis

### Option 1: Using SonarCloud (Recommended for GitHub)

1. Go to https://sonarcloud.io and sign in with GitHub
2. Click "+" → "Analyze new project"
3. Select your repository
4. Follow the setup wizard to get your project key and token
5. Add a GitHub Actions workflow (create `.github/workflows/sonarcloud.yml`):

```yaml
name: SonarCloud Analysis
on:
  push:
    branches:
      - main
      - dev
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  sonarcloud:
    name: SonarCloud
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0  # Shallow clones should be disabled for better analysis
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests with coverage
        run: |
          pytest --cov=. --cov-report=xml
      
      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

6. Create `sonar-project.properties` in your repository root:

```properties
sonar.projectKey=neolisto_simple_python_parser
sonar.organization=neolisto

sonar.sources=.
sonar.exclusions=**/__pycache__/**,**/.pytest_cache/**,**/venv/**
sonar.python.coverage.reportPaths=coverage.xml

sonar.sourceEncoding=UTF-8
```

7. Add the `SONAR_TOKEN` secret to your GitHub repository:
   - Go to your repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `SONAR_TOKEN`
   - Value: Your SonarCloud token

8. Replace `neolisto_simple_python_parser` in README badges with your actual project key

### Option 2: Self-Hosted SonarQube

If you're using a self-hosted SonarQube server, update the badge URLs to point to your server:

```markdown
[![Quality Gate Status](https://your-sonarqube-server.com/api/project_badges/measure?project=neolisto_simple_python_parser&metric=alert_status)](https://your-sonarqube-server.com/dashboard?id=neolisto_simple_python_parser)
```

## License

Add your license information here.

