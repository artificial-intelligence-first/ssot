---
title: GitHub API
slug: github-api
status: living
last_updated: 2025-11-04
tags: [github, api, rest, graphql, webhooks, integration]
summary: "Comprehensive guide to integrating AI agents with GitHub's REST and GraphQL APIs for repository management, automation, and data access."
authors: []
sources:
  - { id: R1, title: "GitHub REST API Documentation", url: "https://docs.github.com/en/rest", accessed: "2025-11-04" }
  - { id: R2, title: "GitHub GraphQL API", url: "https://docs.github.com/en/graphql", accessed: "2025-11-04" }
  - { id: R3, title: "GitHub Webhooks", url: "https://docs.github.com/en/webhooks", accessed: "2025-11-04" }
  - { id: R4, title: "Octokit SDK", url: "https://github.com/octokit", accessed: "2025-11-04" }
---

# GitHub API

> **For Humans**: This document provides comprehensive patterns for integrating AI agents with GitHub's REST and GraphQL APIs. Use this when building tools that interact with GitHub repositories, manage issues and pull requests, or automate development workflows.
>
> **For AI Agents**: Apply these patterns when implementing GitHub API integrations, handling webhooks, or building GitHub-connected applications. Use REST API for simple operations and GraphQL for complex queries.

## Overview

The GitHub API provides programmatic access to GitHub's features and data. This guide focuses on integrating AI agents with GitHub APIs to create intelligent automation, enhance developer workflows, and build sophisticated GitHub-connected applications.

## Authentication

### Personal Access Tokens

```python
from github import Github
from anthropic import Anthropic

# Initialize clients
github_client = Github("ghp_your_token_here")
anthropic_client = Anthropic(api_key="sk-ant-xxx")

# Get authenticated user
user = github_client.get_user()
print(f"Authenticated as: {user.login}")
```

### GitHub App Authentication

```python
import jwt
import time
import requests

def generate_jwt(app_id, private_key):
    """Generate JWT for GitHub App authentication."""
    payload = {
        'iat': int(time.time()),
        'exp': int(time.time()) + (10 * 60),  # 10 minutes
        'iss': app_id
    }

    return jwt.encode(payload, private_key, algorithm='RS256')

def get_installation_token(app_id, private_key, installation_id):
    """Get installation access token."""
    jwt_token = generate_jwt(app_id, private_key)

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.post(
        f'https://api.github.com/app/installations/{installation_id}/access_tokens',
        headers=headers
    )

    return response.json()['token']
```

### OAuth App Flow

```python
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

@app.route('/login')
def login():
    """Initiate OAuth flow."""
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&scope=repo,user"
    return redirect(github_auth_url)

@app.route('/callback')
def callback():
    """Handle OAuth callback."""
    code = request.args.get('code')

    # Exchange code for access token
    response = requests.post(
        'https://github.com/login/oauth/access_token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code
        },
        headers={'Accept': 'application/json'}
    )

    access_token = response.json()['access_token']
    return f"Access token: {access_token}"
```

## REST API Integration

### Repository Operations

```python
from github import Github
from anthropic import Anthropic

class GitHubAIAssistant:
    """AI-powered GitHub repository assistant."""

    def __init__(self, github_token: str, anthropic_api_key: str):
        self.github = Github(github_token)
        self.anthropic = Anthropic(api_key=anthropic_api_key)

    def analyze_repository(self, repo_name: str):
        """Analyze repository structure and provide insights."""
        repo = self.github.get_repo(repo_name)

        # Gather repository information
        context = {
            'name': repo.name,
            'description': repo.description,
            'language': repo.language,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'open_issues': repo.open_issues_count,
            'topics': repo.get_topics()
        }

        # Get recent commits
        commits = repo.get_commits()[:10]
        recent_activity = [
            f"{c.commit.author.date}: {c.commit.message}"
            for c in commits
        ]

        # AI analysis
        response = self.anthropic.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=2048,
            messages=[{
                'role': 'user',
                'content': f"""Analyze this GitHub repository:

Repository: {context}
Recent Activity: {recent_activity}

Provide:
1. Overview and purpose
2. Activity assessment
3. Health indicators
4. Recommendations for improvement
"""
            }]
        )

        return response.content[0].text

    def create_issue_from_analysis(self, repo_name: str, analysis: str):
        """Create GitHub issue from AI analysis."""
        repo = self.github.get_repo(repo_name)

        issue = repo.create_issue(
            title="🤖 AI Repository Analysis",
            body=f"""## Automated Repository Analysis

{analysis}

---
*This issue was automatically created by an AI assistant.*
""",
            labels=['automated', 'analysis']
        )

        return issue
```

### Issue Management

```python
class IssueManager:
    """AI-powered GitHub issue management."""

    def __init__(self, github_client, anthropic_client):
        self.github = github_client
        self.anthropic = anthropic_client

    def triage_issues(self, repo_name: str):
        """Automatically triage and label issues."""
        repo = self.github.get_repo(repo_name)
        issues = repo.get_issues(state='open', labels=['needs-triage'])

        for issue in issues:
            # Analyze issue with AI
            analysis = self.analyze_issue(issue)

            # Apply labels
            issue.add_to_labels(*analysis['labels'])

            # Set priority
            if analysis['priority'] == 'high':
                issue.add_to_labels('priority: high')

            # Add comment with analysis
            issue.create_comment(
                f"🤖 **Automated Triage**\n\n"
                f"Category: {analysis['category']}\n"
                f"Priority: {analysis['priority']}\n"
                f"Suggested Labels: {', '.join(analysis['labels'])}\n\n"
                f"Analysis: {analysis['summary']}"
            )

            # Remove triage label
            issue.remove_from_labels('needs-triage')

    def analyze_issue(self, issue):
        """Analyze issue using AI."""
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
- category: bug|feature|documentation|question
- priority: low|medium|high|critical
- labels: array of relevant labels
- summary: brief analysis
"""
            }]
        )

        import json
        return json.loads(response.content[0].text)

    def suggest_related_issues(self, repo_name: str, issue_number: int):
        """Find and suggest related issues."""
        repo = self.github.get_repo(repo_name)
        issue = repo.get_issue(issue_number)

        # Get all issues
        all_issues = repo.get_issues(state='all')

        # Prepare context for AI
        issue_summaries = [
            f"#{i.number}: {i.title}"
            for i in all_issues
            if i.number != issue_number
        ][:50]  # Limit to recent 50

        # Find related issues using AI
        response = self.anthropic.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=1024,
            messages=[{
                'role': 'user',
                'content': f"""Find issues related to:

Current Issue: #{issue.number} - {issue.title}
Description: {issue.body}

Available Issues:
{chr(10).join(issue_summaries)}

Return JSON array of related issue numbers with relevance scores.
"""
            }]
        )

        import json
        related = json.loads(response.content[0].text)

        # Comment with suggestions
        if related:
            links = [
                f"- #{num} (relevance: {score})"
                for num, score in related[:5]
            ]
            issue.create_comment(
                f"🔗 **Related Issues**\n\n" + "\n".join(links)
            )
```

### Pull Request Management

```python
class PRManager:
    """AI-powered pull request management."""

    def __init__(self, github_client, anthropic_client):
        self.github = github_client
        self.anthropic = anthropic_client

    def review_pr(self, repo_name: str, pr_number: int):
        """Perform AI code review on pull request."""
        repo = self.github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        # Get changed files
        files = pr.get_files()

        reviews = []
        for file in files:
            # Skip large files
            if file.changes > 500:
                continue

            # Get file content
            if file.status == 'removed':
                continue

            # AI review
            review = self.review_file(file)
            reviews.append(review)

        # Create review comment
        self.create_review(pr, reviews)

    def review_file(self, file):
        """Review a single file."""
        response = self.anthropic.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=2048,
            messages=[{
                'role': 'user',
                'content': f"""Review this code change:

File: {file.filename}
Changes: +{file.additions} -{file.deletions}

Patch:
{file.patch}

Provide:
1. Code quality assessment
2. Potential issues or bugs
3. Security concerns
4. Performance implications
5. Suggestions for improvement

Format as JSON with: {{issues: [], suggestions: [], score: 0-100}}
"""
            }]
        )

        import json
        return {
            'file': file.filename,
            'analysis': json.loads(response.content[0].text)
        }

    def create_review(self, pr, reviews):
        """Create review comment on PR."""
        # Generate summary
        summary = self.generate_review_summary(reviews)

        # Create review
        pr.create_review(
            body=summary,
            event='COMMENT'
        )

        # Add inline comments for specific issues
        for review in reviews:
            for issue in review['analysis'].get('issues', []):
                if 'line' in issue:
                    pr.create_review_comment(
                        body=f"⚠️ {issue['message']}\n\n{issue.get('suggestion', '')}",
                        path=review['file'],
                        line=issue['line']
                    )

    def generate_review_summary(self, reviews):
        """Generate overall review summary."""
        response = self.anthropic.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=1024,
            messages=[{
                'role': 'user',
                'content': f"""Generate a code review summary:

Reviews: {reviews}

Create a concise summary with:
- Overall assessment
- Key findings
- Recommended actions
"""
            }]
        )

        return f"🤖 **AI Code Review**\n\n{response.content[0].text}"

    def auto_merge_ready(self, repo_name: str, pr_number: int):
        """Check if PR is ready for auto-merge."""
        repo = self.github.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        # Check requirements
        checks = {
            'approved': self.is_approved(pr),
            'tests_passing': self.tests_passing(pr),
            'no_conflicts': not pr.mergeable_state == 'dirty',
            'up_to_date': self.is_up_to_date(pr)
        }

        if all(checks.values()):
            pr.merge(merge_method='squash')
            return True

        return False
```

## GraphQL API Integration

### Complex Queries

```python
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

class GitHubGraphQL:
    """GraphQL API client for GitHub."""

    def __init__(self, token: str):
        transport = RequestsHTTPTransport(
            url='https://api.github.com/graphql',
            headers={'Authorization': f'bearer {token}'},
            use_json=True
        )
        self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def get_repository_insights(self, owner: str, name: str):
        """Get comprehensive repository insights."""
        query = gql("""
            query($owner: String!, $name: String!) {
              repository(owner: $owner, name: $name) {
                name
                description
                stargazerCount
                forkCount
                issues(first: 10, states: OPEN, orderBy: {field: CREATED_AT, direction: DESC}) {
                  nodes {
                    number
                    title
                    author {
                      login
                    }
                    createdAt
                    labels(first: 5) {
                      nodes {
                        name
                      }
                    }
                  }
                }
                pullRequests(first: 10, states: OPEN, orderBy: {field: CREATED_AT, direction: DESC}) {
                  nodes {
                    number
                    title
                    author {
                      login
                    }
                    createdAt
                    reviews(first: 5) {
                      nodes {
                        state
                        author {
                          login
                        }
                      }
                    }
                  }
                }
                languages(first: 10) {
                  edges {
                    node {
                      name
                    }
                    size
                  }
                }
              }
            }
        """)

        result = self.client.execute(query, variable_values={
            'owner': owner,
            'name': name
        })

        return result

    def get_user_activity(self, username: str):
        """Get user's recent activity across repositories."""
        query = gql("""
            query($username: String!) {
              user(login: $username) {
                contributionsCollection {
                  totalCommitContributions
                  totalIssueContributions
                  totalPullRequestContributions
                  totalPullRequestReviewContributions
                  commitContributionsByRepository(maxRepositories: 10) {
                    repository {
                      name
                      owner {
                        login
                      }
                    }
                    contributions {
                      totalCount
                    }
                  }
                }
                pullRequests(first: 10, orderBy: {field: CREATED_AT, direction: DESC}) {
                  nodes {
                    title
                    repository {
                      name
                    }
                    createdAt
                    state
                  }
                }
              }
            }
        """)

        result = self.client.execute(query, variable_values={
            'username': username
        })

        return result

    def analyze_team_velocity(self, org: str, team: str):
        """Analyze team's development velocity."""
        query = gql("""
            query($org: String!, $team: String!) {
              organization(login: $org) {
                team(slug: $team) {
                  members(first: 50) {
                    nodes {
                      login
                      contributionsCollection {
                        totalCommitContributions
                        totalPullRequestContributions
                        totalPullRequestReviewContributions
                      }
                    }
                  }
                }
              }
            }
        """)

        result = self.client.execute(query, variable_values={
            'org': org,
            'team': team
        })

        return result
```

### Mutations

```python
def create_issue_with_graphql(self, repo_id: str, title: str, body: str):
    """Create issue using GraphQL mutation."""
    mutation = gql("""
        mutation($repositoryId: ID!, $title: String!, $body: String!) {
          createIssue(input: {
            repositoryId: $repositoryId
            title: $title
            body: $body
          }) {
            issue {
              number
              url
            }
          }
        }
    """)

    result = self.client.execute(mutation, variable_values={
        'repositoryId': repo_id,
        'title': title,
        'body': body
    })

    return result

def add_comment(self, subject_id: str, body: str):
    """Add comment to issue or PR."""
    mutation = gql("""
        mutation($subjectId: ID!, $body: String!) {
          addComment(input: {
            subjectId: $subjectId
            body: $body
          }) {
            commentEdge {
              node {
                id
                url
              }
            }
          }
        }
    """)

    result = self.client.execute(mutation, variable_values={
        'subjectId': subject_id,
        'body': body
    })

    return result
```

## Webhooks

### Webhook Server

```python
from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

WEBHOOK_SECRET = "your_webhook_secret"

def verify_signature(payload, signature):
    """Verify GitHub webhook signature."""
    expected = 'sha256=' + hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)

@app.route('/webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events."""
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if not verify_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401

    # Get event type
    event_type = request.headers.get('X-GitHub-Event')

    # Parse payload
    payload = request.json

    # Route to appropriate handler
    if event_type == 'push':
        handle_push(payload)
    elif event_type == 'pull_request':
        handle_pull_request(payload)
    elif event_type == 'issues':
        handle_issue(payload)
    elif event_type == 'issue_comment':
        handle_issue_comment(payload)

    return jsonify({'status': 'success'}), 200

def handle_push(payload):
    """Handle push events."""
    repo = payload['repository']['full_name']
    commits = payload['commits']

    print(f"Push to {repo}: {len(commits)} commits")

    # AI analysis of commit messages
    anthropic_client = Anthropic()
    commit_messages = [c['message'] for c in commits]

    response = anthropic_client.messages.create(
        model='claude-3-5-sonnet-20241022',
        max_tokens=1024,
        messages=[{
            'role': 'user',
            'content': f"""Analyze these commit messages:

{chr(10).join(commit_messages)}

Are they following best practices? Suggest improvements.
"""
        }]
    )

    # Could post analysis back to repository

def handle_pull_request(payload):
    """Handle pull request events."""
    action = payload['action']
    pr = payload['pull_request']

    if action == 'opened':
        # Trigger AI review
        print(f"New PR #{pr['number']}: {pr['title']}")

def handle_issue(payload):
    """Handle issue events."""
    action = payload['action']
    issue = payload['issue']

    if action == 'opened':
        # Auto-triage new issues
        print(f"New issue #{issue['number']}: {issue['title']}")

def handle_issue_comment(payload):
    """Handle issue comment events."""
    comment = payload['comment']
    issue = payload['issue']

    # Check if bot is mentioned
    if '@ai-assistant' in comment['body']:
        # Respond to mention
        print(f"Bot mentioned in issue #{issue['number']}")
```

### Event Processing

```python
class WebhookProcessor:
    """Process GitHub webhook events with AI."""

    def __init__(self, github_client, anthropic_client):
        self.github = github_client
        self.anthropic = anthropic_client

    def process_new_issue(self, payload):
        """Process new issue creation."""
        repo_name = payload['repository']['full_name']
        issue = payload['issue']

        # Analyze issue
        analysis = self.analyze_issue_content(
            issue['title'],
            issue['body']
        )

        # Auto-label
        repo = self.github.get_repo(repo_name)
        gh_issue = repo.get_issue(issue['number'])
        gh_issue.add_to_labels(*analysis['labels'])

        # Add helpful comment
        if analysis.get('needs_info'):
            gh_issue.create_comment(
                "🤖 Thank you for opening this issue! "
                "To help us better understand, could you please provide:\n\n"
                + "\n".join(f"- {item}" for item in analysis['needs_info'])
            )

    def process_pr_review_request(self, payload):
        """Process PR review request."""
        repo_name = payload['repository']['full_name']
        pr = payload['pull_request']

        # Get PR diff
        repo = self.github.get_repo(repo_name)
        gh_pr = repo.get_pull(pr['number'])

        # Perform AI review
        review = self.review_pr_changes(gh_pr)

        # Post review
        gh_pr.create_review(
            body=review['summary'],
            event='COMMENT',
            comments=review['comments']
        )

    def analyze_issue_content(self, title, body):
        """Analyze issue content."""
        response = self.anthropic.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=1024,
            messages=[{
                'role': 'user',
                'content': f"""Analyze this issue:

Title: {title}
Body: {body}

Return JSON with:
- labels: suggested labels
- needs_info: missing information
- priority: estimated priority
"""
            }]
        )

        import json
        return json.loads(response.content[0].text)
```

## SDK Integration

### Octokit.js

```javascript
import { Octokit } from '@octokit/rest';
import Anthropic from '@anthropic-ai/sdk';

class GitHubAIBot {
  constructor(githubToken, anthropicKey) {
    this.octokit = new Octokit({ auth: githubToken });
    this.anthropic = new Anthropic({ apiKey: anthropicKey });
  }

  async analyzeRepository(owner, repo) {
    // Get repository data
    const { data: repository } = await this.octokit.repos.get({
      owner,
      repo
    });

    const { data: languages } = await this.octokit.repos.listLanguages({
      owner,
      repo
    });

    const { data: commits } = await this.octokit.repos.listCommits({
      owner,
      repo,
      per_page: 20
    });

    // AI analysis
    const response = await this.anthropic.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 2048,
      messages: [{
        role: 'user',
        content: `Analyze this repository:

        Name: ${repository.name}
        Description: ${repository.description}
        Stars: ${repository.stargazers_count}
        Languages: ${JSON.stringify(languages)}
        Recent commits: ${commits.length}

        Provide insights about the project's health and activity.`
      }]
    });

    return response.content[0].text;
  }

  async autoRespondToIssues(owner, repo) {
    // Get recent issues
    const { data: issues } = await this.octokit.issues.listForRepo({
      owner,
      repo,
      state: 'open',
      labels: 'needs-response',
      per_page: 10
    });

    for (const issue of issues) {
      // Generate AI response
      const response = await this.anthropic.messages.create({
        model: 'claude-3-5-sonnet-20241022',
        max_tokens: 1024,
        messages: [{
          role: 'user',
          content: `Generate a helpful response to this GitHub issue:

          Title: ${issue.title}
          Body: ${issue.body}

          Be friendly, professional, and helpful.`
        }]
      });

      // Post comment
      await this.octokit.issues.createComment({
        owner,
        repo,
        issue_number: issue.number,
        body: `🤖 ${response.content[0].text}\n\n---\n*This response was generated by an AI assistant.*`
      });

      // Remove label
      await this.octokit.issues.removeLabel({
        owner,
        repo,
        issue_number: issue.number,
        name: 'needs-response'
      });
    }
  }
}
```

### PyGithub

```python
from github import Github
from anthropic import Anthropic
import time

class GitHubMonitor:
    """Monitor GitHub repositories with AI assistance."""

    def __init__(self, github_token: str, anthropic_key: str):
        self.github = Github(github_token)
        self.anthropic = Anthropic(api_key=anthropic_key)

    def monitor_repository(self, repo_name: str, interval: int = 300):
        """Monitor repository for activity."""
        repo = self.github.get_repo(repo_name)
        last_check = time.time()

        while True:
            # Check for new issues
            issues = repo.get_issues(
                state='open',
                since=time.time() - interval
            )

            for issue in issues:
                self.process_new_issue(repo, issue)

            # Check for new PRs
            pulls = repo.get_pulls(
                state='open',
                sort='created',
                direction='desc'
            )

            for pr in pulls[:5]:  # Check 5 most recent
                if (time.time() - pr.created_at.timestamp()) < interval:
                    self.process_new_pr(repo, pr)

            time.sleep(interval)

    def process_new_issue(self, repo, issue):
        """Process newly created issue."""
        # Auto-triage
        labels = self.suggest_labels(issue)
        issue.add_to_labels(*labels)

        # Check if needs immediate attention
        if self.is_urgent(issue):
            issue.add_to_labels('urgent')
            # Notify team

    def suggest_labels(self, issue):
        """Suggest labels for issue."""
        response = self.anthropic.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=512,
            messages=[{
                'role': 'user',
                'content': f"""Suggest labels for this issue:

{issue.title}
{issue.body}

Return comma-separated labels.
"""
            }]
        )

        return [l.strip() for l in response.content[0].text.split(',')]
```

## Rate Limiting

### Handling Rate Limits

```python
import time
from github import RateLimitExceededException

class RateLimitedGitHub:
    """GitHub client with rate limit handling."""

    def __init__(self, token: str):
        self.client = Github(token)

    def safe_api_call(self, func, *args, **kwargs):
        """Make API call with rate limit handling."""
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                return func(*args, **kwargs)
            except RateLimitExceededException:
                # Check rate limit
                rate_limit = self.client.get_rate_limit()
                reset_time = rate_limit.core.reset

                # Calculate wait time
                wait_seconds = (reset_time - time.time()) + 10

                print(f"Rate limit exceeded. Waiting {wait_seconds}s")
                time.sleep(wait_seconds)

                retry_count += 1

        raise Exception("Max retries exceeded")

    def batch_operations(self, operations, batch_size=10):
        """Perform operations in batches to manage rate limits."""
        results = []

        for i in range(0, len(operations), batch_size):
            batch = operations[i:i + batch_size]

            for op in batch:
                result = self.safe_api_call(op)
                results.append(result)

            # Check remaining rate limit
            rate_limit = self.client.get_rate_limit()
            if rate_limit.core.remaining < 100:
                print("Low rate limit, slowing down...")
                time.sleep(60)

        return results
```

## Best Practices

### Error Handling

```python
from github import GithubException
import logging

logger = logging.getLogger(__name__)

def safe_github_operation(operation):
    """Safely execute GitHub operation."""
    try:
        return operation()
    except GithubException as e:
        if e.status == 404:
            logger.error("Resource not found")
        elif e.status == 403:
            logger.error("Permission denied")
        elif e.status == 422:
            logger.error("Validation failed")
        else:
            logger.error(f"GitHub API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return None
```

### Caching

```python
from functools import lru_cache
import pickle
import os

class CachedGitHubClient:
    """GitHub client with caching."""

    def __init__(self, token: str, cache_dir='.github_cache'):
        self.client = Github(token)
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_cached_or_fetch(self, key, fetch_func, ttl=3600):
        """Get from cache or fetch if expired."""
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")

        # Check cache
        if os.path.exists(cache_file):
            age = time.time() - os.path.getmtime(cache_file)
            if age < ttl:
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)

        # Fetch and cache
        data = fetch_func()
        with open(cache_file, 'wb') as f:
            pickle.dump(data, f)

        return data
```

## See Also

- [GitHub Actions](./actions.md) - CI/CD automation
- [GitHub Apps](./apps.md) - Building GitHub Apps
- [AGENTS.md](../../../AGENTS.md) - Operational documentation

## References

- [R1] GitHub REST API Documentation. https://docs.github.com/en/rest (accessed 2025-11-04)
- [R2] GitHub GraphQL API. https://docs.github.com/en/graphql (accessed 2025-11-04)
- [R3] GitHub Webhooks. https://docs.github.com/en/webhooks (accessed 2025-11-04)
- [R4] Octokit SDK. https://github.com/octokit (accessed 2025-11-04)
