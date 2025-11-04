---
title: GitHub Apps
slug: github-apps
status: living
last_updated: 2025-11-04
tags: [github, apps, oauth, integration, automation]
summary: "Guide to building GitHub Apps with AI capabilities for enhanced repository automation and intelligent workflows."
authors: []
sources:
  - { id: R1, title: "GitHub Apps Documentation", url: "https://docs.github.com/en/apps", accessed: "2025-11-04" }
  - { id: R2, title: "Building GitHub Apps", url: "https://docs.github.com/en/apps/creating-github-apps", accessed: "2025-11-04" }
  - { id: R3, title: "Authenticating with GitHub Apps", url: "https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app", accessed: "2025-11-04" }
---

# GitHub Apps

> **For Humans**: This document explains how to build AI-powered GitHub Apps that enhance repository workflows with intelligent automation. Use this when creating applications that need deep GitHub integration with AI capabilities.
>
> **For AI Agents**: Apply these patterns when building GitHub Apps, implementing app authentication, or creating intelligent repository automation tools.

## Overview

GitHub Apps are first-class actors within GitHub that can perform actions via the API and integrate with user workflows. Combined with AI, they enable intelligent automation, code review, issue management, and more.

## Creating a GitHub App

### App Configuration

1. Navigate to Settings > Developer settings > GitHub Apps > New GitHub App
2. Configure basic information:
   - **Name**: Your app name
   - **Homepage URL**: Your app's website
   - **Webhook URL**: Endpoint for receiving events
   - **Webhook secret**: Secret for verifying payloads

3. Set permissions:
   - Repository permissions
   - Organization permissions
   - User permissions

4. Subscribe to events:
   - Issues
   - Pull requests
   - Push
   - Repository
   - etc.

### App Manifest

```json
{
  "name": "AI Code Assistant",
  "url": "https://example.com",
  "hook_attributes": {
    "url": "https://example.com/webhook"
  },
  "redirect_url": "https://example.com/auth/callback",
  "public": true,
  "default_permissions": {
    "issues": "write",
    "pull_requests": "write",
    "contents": "read",
    "metadata": "read"
  },
  "default_events": [
    "issues",
    "pull_request",
    "push"
  ]
}
```

## Authentication

### JWT Authentication

```python
import jwt
import time
from datetime import datetime, timedelta

class GitHubAppAuth:
    """Handle GitHub App authentication."""

    def __init__(self, app_id: str, private_key: str):
        self.app_id = app_id
        self.private_key = private_key

    def generate_jwt(self) -> str:
        """Generate JWT for GitHub App."""
        now = int(time.time())

        payload = {
            'iat': now,
            'exp': now + (10 * 60),  # 10 minutes
            'iss': self.app_id
        }

        return jwt.encode(
            payload,
            self.private_key,
            algorithm='RS256'
        )

    def get_installation_token(self, installation_id: str) -> dict:
        """Get installation access token."""
        import requests

        jwt_token = self.generate_jwt()

        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        url = f'https://api.github.com/app/installations/{installation_id}/access_tokens'
        response = requests.post(url, headers=headers)

        return response.json()
```

### Installation Access Token

```python
from github import GithubIntegration

class GitHubAppClient:
    """GitHub App API client."""

    def __init__(self, app_id: str, private_key_path: str):
        with open(private_key_path, 'r') as f:
            private_key = f.read()

        self.integration = GithubIntegration(app_id, private_key)

    def get_installation_client(self, installation_id: int):
        """Get GitHub client for installation."""
        token = self.integration.get_access_token(installation_id).token
        return Github(token)

    def get_installations(self):
        """Get all installations of the app."""
        return self.integration.get_installations()
```

## Building AI-Powered Apps

### Code Review Bot

```python
from github import Github
from anthropic import Anthropic
import os

class AICodeReviewBot:
    """AI-powered code review bot."""

    def __init__(self, installation_id: int):
        # Initialize GitHub App client
        self.github_app = GitHubAppClient(
            app_id=os.environ['GITHUB_APP_ID'],
            private_key_path='private-key.pem'
        )
        self.github = self.github_app.get_installation_client(installation_id)

        # Initialize AI client
        self.anthropic = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

    def review_pull_request(self, repo_name: str, pr_number: int):
        """Perform AI code review on pull request."""
        repo = self.github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        # Get changed files
        files = pr.get_files()

        review_comments = []

        for file in files:
            if file.changes > 500:
                continue  # Skip very large files

            # Review file with AI
            comments = self.review_file(file)
            review_comments.extend(comments)

        # Post review
        self.post_review(pr, review_comments)

    def review_file(self, file):
        """Review a single file with AI."""
        response = self.anthropic.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=2048,
            messages=[{
                'role': 'user',
                'content': f"""Review this code change:

File: {file.filename}
Status: {file.status}
Changes: +{file.additions} -{file.deletions}

Patch:
```
{file.patch}
```

Provide specific, actionable feedback focusing on:
1. Bugs or potential issues
2. Security concerns
3. Performance problems
4. Code quality and best practices

Return JSON array of comments with: {{line, severity, message, suggestion}}
"""
            }]
        )

        import json
        try:
            comments = json.loads(response.content[0].text)
            return [{
                'path': file.filename,
                'line': comment['line'],
                'body': f"**{comment['severity']}**: {comment['message']}\n\n{comment.get('suggestion', '')}"
            } for comment in comments]
        except json.JSONDecodeError:
            return []

    def post_review(self, pr, comments):
        """Post review to pull request."""
        if not comments:
            pr.create_review(
                body="✅ AI review found no issues.",
                event='COMMENT'
            )
            return

        # Group comments by file
        review_body = "🤖 **AI Code Review**\n\nI've analyzed the changes and have some suggestions."

        pr.create_review(
            body=review_body,
            event='COMMENT',
            comments=comments
        )
```

### Issue Triage Bot

```python
class AIIssueTriageBot:
    """AI-powered issue triage bot."""

    def __init__(self, installation_id: int):
        self.github_app = GitHubAppClient(
            app_id=os.environ['GITHUB_APP_ID'],
            private_key_path='private-key.pem'
        )
        self.github = self.github_app.get_installation_client(installation_id)
        self.anthropic = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

    def triage_issue(self, repo_name: str, issue_number: int):
        """Automatically triage an issue."""
        repo = self.github.get_repo(repo_name)
        issue = repo.get_issue(issue_number)

        # Analyze issue with AI
        analysis = self.analyze_issue(issue)

        # Apply labels
        labels = analysis.get('labels', [])
        if labels:
            issue.add_to_labels(*labels)

        # Add priority label
        priority = analysis.get('priority')
        if priority:
            issue.add_to_labels(f'priority: {priority}')

        # Add category label
        category = analysis.get('category')
        if category:
            issue.add_to_labels(f'category: {category}')

        # Post analysis comment
        self.post_triage_comment(issue, analysis)

        # Assign if appropriate
        if analysis.get('auto_assign'):
            assignee = analysis['auto_assign']
            issue.add_to_assignees(assignee)

    def analyze_issue(self, issue):
        """Analyze issue with AI."""
        response = self.anthropic.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=1024,
            messages=[{
                'role': 'user',
                'content': f"""Analyze this GitHub issue:

Title: {issue.title}
Body: {issue.body}
Author: {issue.user.login}
Created: {issue.created_at}

Provide JSON with:
- category: bug|feature|documentation|question|other
- priority: low|medium|high|critical
- labels: array of relevant labels
- summary: brief analysis
- auto_assign: username if issue should be auto-assigned (or null)
- needs_info: boolean indicating if more information is needed
"""
            }]
        )

        import json
        return json.loads(response.content[0].text)

    def post_triage_comment(self, issue, analysis):
        """Post triage analysis as comment."""
        comment = f"""🤖 **Automated Triage**

**Category**: {analysis['category']}
**Priority**: {analysis['priority']}
**Summary**: {analysis['summary']}

**Suggested Labels**: {', '.join(analysis.get('labels', []))}
"""

        if analysis.get('needs_info'):
            comment += "\n\n⚠️ **Additional Information Needed**\nPlease provide more details to help us address this issue."

        issue.create_comment(comment)
```

### Documentation Bot

```python
class AIDocumentationBot:
    """AI-powered documentation bot."""

    def __init__(self, installation_id: int):
        self.github_app = GitHubAppClient(
            app_id=os.environ['GITHUB_APP_ID'],
            private_key_path='private-key.pem'
        )
        self.github = self.github_app.get_installation_client(installation_id)
        self.anthropic = Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

    def generate_docs_for_pr(self, repo_name: str, pr_number: int):
        """Generate documentation for code in PR."""
        repo = self.github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        # Get changed files
        files = pr.get_files()

        docs = []

        for file in files:
            # Only process code files
            if not self.is_code_file(file.filename):
                continue

            # Generate documentation
            doc = self.generate_documentation(file)
            docs.append(doc)

        if docs:
            # Create documentation file
            self.commit_documentation(repo, pr, docs)

    def is_code_file(self, filename: str) -> bool:
        """Check if file is a code file."""
        code_extensions = ['.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c']
        return any(filename.endswith(ext) for ext in code_extensions)

    def generate_documentation(self, file):
        """Generate documentation for a file."""
        response = self.anthropic.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=2048,
            messages=[{
                'role': 'user',
                'content': f"""Generate comprehensive documentation for this code:

File: {file.filename}

Code:
```
{file.patch}
```

Generate documentation including:
- Overview
- Functions/Classes with parameters and return values
- Usage examples
- Notes on important behavior

Format as Markdown.
"""
            }]
        )

        return {
            'filename': file.filename,
            'documentation': response.content[0].text
        }

    def commit_documentation(self, repo, pr, docs):
        """Commit generated documentation."""
        # Create documentation content
        doc_content = "# Auto-Generated Documentation\n\n"

        for doc in docs:
            doc_content += f"## {doc['filename']}\n\n{doc['documentation']}\n\n"

        # Get PR branch
        branch = pr.head.ref

        # Create/update docs file
        doc_path = "docs/GENERATED.md"

        try:
            # Try to get existing file
            contents = repo.get_contents(doc_path, ref=branch)
            repo.update_file(
                doc_path,
                "docs: update auto-generated documentation",
                doc_content,
                contents.sha,
                branch=branch
            )
        except:
            # File doesn't exist, create it
            repo.create_file(
                doc_path,
                "docs: add auto-generated documentation",
                doc_content,
                branch=branch
            )

        # Comment on PR
        pr.create_comment(
            "📚 I've generated documentation for the code changes in this PR. "
            f"You can find it in `{doc_path}`."
        )
```

## Webhook Handling

### Flask Webhook Server

```python
from flask import Flask, request, jsonify
import hmac
import hashlib
import os

app = Flask(__name__)

WEBHOOK_SECRET = os.environ['GITHUB_WEBHOOK_SECRET']

def verify_webhook_signature(payload_body, signature_header):
    """Verify GitHub webhook signature."""
    if not signature_header:
        return False

    hash_algorithm, github_signature = signature_header.split('=')

    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        msg=payload_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, github_signature)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle GitHub webhook events."""
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_webhook_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401

    # Get event type
    event_type = request.headers.get('X-GitHub-Event')

    # Get installation ID
    payload = request.json
    installation_id = payload.get('installation', {}).get('id')

    if not installation_id:
        return jsonify({'error': 'No installation ID'}), 400

    # Route to appropriate handler
    if event_type == 'pull_request':
        handle_pull_request(payload, installation_id)
    elif event_type == 'issues':
        handle_issues(payload, installation_id)
    elif event_type == 'push':
        handle_push(payload, installation_id)
    elif event_type == 'installation':
        handle_installation(payload)

    return jsonify({'status': 'success'}), 200

def handle_pull_request(payload, installation_id):
    """Handle pull request events."""
    action = payload['action']
    pr = payload['pull_request']
    repo = payload['repository']['full_name']

    if action in ['opened', 'synchronize']:
        # Trigger AI code review
        bot = AICodeReviewBot(installation_id)
        bot.review_pull_request(repo, pr['number'])

def handle_issues(payload, installation_id):
    """Handle issue events."""
    action = payload['action']
    issue = payload['issue']
    repo = payload['repository']['full_name']

    if action == 'opened':
        # Trigger AI triage
        bot = AIIssueTriageBot(installation_id)
        bot.triage_issue(repo, issue['number'])

def handle_push(payload, installation_id):
    """Handle push events."""
    repo = payload['repository']['full_name']
    commits = payload['commits']

    # Could trigger documentation generation, etc.
    pass

def handle_installation(payload):
    """Handle installation events."""
    action = payload['action']
    installation = payload['installation']

    if action == 'created':
        print(f"App installed: {installation['id']}")
    elif action == 'deleted':
        print(f"App uninstalled: {installation['id']}")
```

### FastAPI Webhook Server

```python
from fastapi import FastAPI, Request, HTTPException, Header
from typing import Optional
import hmac
import hashlib

app = FastAPI()

async def verify_signature(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None)
):
    """Verify webhook signature."""
    if not x_hub_signature_256:
        raise HTTPException(status_code=401, detail="No signature")

    body = await request.body()
    expected = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

@app.post("/webhook")
async def webhook(
    request: Request,
    x_github_event: str = Header(...),
    x_hub_signature_256: str = Header(...)
):
    """Handle GitHub webhooks."""
    # Verify signature
    await verify_signature(request, x_hub_signature_256)

    # Parse payload
    payload = await request.json()
    installation_id = payload.get('installation', {}).get('id')

    # Route based on event type
    if x_github_event == 'pull_request':
        await handle_pull_request(payload, installation_id)
    elif x_github_event == 'issues':
        await handle_issues(payload, installation_id)

    return {"status": "success"}
```

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "4", "app:app"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: github-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: github-app
  template:
    metadata:
      labels:
        app: github-app
    spec:
      containers:
      - name: app
        image: github-app:latest
        ports:
        - containerPort: 8000
        env:
        - name: GITHUB_APP_ID
          valueFrom:
            secretKeyRef:
              name: github-app-secrets
              key: app-id
        - name: GITHUB_WEBHOOK_SECRET
          valueFrom:
            secretKeyRef:
              name: github-app-secrets
              key: webhook-secret
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: github-app-secrets
              key: anthropic-key
        volumeMounts:
        - name: private-key
          mountPath: /app/private-key.pem
          subPath: private-key.pem
          readOnly: true
      volumes:
      - name: private-key
        secret:
          secretName: github-app-private-key
---
apiVersion: v1
kind: Service
metadata:
  name: github-app
spec:
  selector:
    app: github-app
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

## Best Practices

### 1. Secure Secrets Management

```python
import os
from cryptography.fernet import Fernet

class SecureConfig:
    """Secure configuration management."""

    def __init__(self):
        self.encryption_key = os.environ['ENCRYPTION_KEY']
        self.cipher = Fernet(self.encryption_key.encode())

    def get_secret(self, name: str) -> str:
        """Get decrypted secret."""
        encrypted = os.environ.get(name)
        if not encrypted:
            raise ValueError(f"Secret {name} not found")

        return self.cipher.decrypt(encrypted.encode()).decode()
```

### 2. Rate Limiting

```python
from functools import wraps
import time

class RateLimiter:
    """Rate limiter for API calls."""

    def __init__(self, max_calls: int, period: int):
        self.max_calls = max_calls
        self.period = period
        self.calls = []

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()

            # Remove old calls
            self.calls = [c for c in self.calls if c > now - self.period]

            # Check limit
            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                time.sleep(sleep_time)

            # Add current call
            self.calls.append(time.time())

            return func(*args, **kwargs)

        return wrapper
```

### 3. Error Handling

```python
import logging
from functools import wraps

logger = logging.getLogger(__name__)

def handle_errors(func):
    """Decorator for error handling."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}", exc_info=True)
            # Could send to error tracking service
            raise
    return wrapper
```

## Monitoring

### Logging

```python
import logging
from pythonjsonlogger import jsonlogger

# Setup JSON logging
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

# Log events
logger.info("Webhook received", extra={
    'event_type': 'pull_request',
    'repo': 'owner/repo',
    'installation_id': 12345
})
```

### Metrics

```python
from prometheus_client import Counter, Histogram
import time

# Define metrics
webhook_requests = Counter('webhook_requests_total', 'Total webhook requests', ['event_type'])
review_duration = Histogram('review_duration_seconds', 'Time to complete review')

@webhook_requests.labels(event_type='pull_request').count_exceptions()
@review_duration.time()
def review_pull_request(repo, pr_number):
    """Review PR with metrics."""
    # Review logic
    pass
```

## See Also

- [GitHub API](./api.md) - REST and GraphQL APIs
- [GitHub Actions](./actions.md) - CI/CD automation
- [AGENTS.md](../../../AGENTS.md) - Operational documentation

## References

- [R1] GitHub Apps Documentation. https://docs.github.com/en/apps (accessed 2025-11-04)
- [R2] Building GitHub Apps. https://docs.github.com/en/apps/creating-github-apps (accessed 2025-11-04)
- [R3] Authenticating with GitHub Apps. https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app (accessed 2025-11-04)
