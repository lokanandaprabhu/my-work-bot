"""
GitHub API Client for fetching pull requests and related data.
"""
import os
import requests
from typing import List, Dict, Optional


class GitHubClient:
    """Client to interact with GitHub REST API v3."""
    
    def __init__(self, token: str, org: str, username: str, repos: Optional[List[str]] = None):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub personal access token
            org: GitHub organization name
            username: GitHub username to query for
            repos: Optional list of specific repos to check
        """
        self.token = token
        self.org = org
        self.username = username
        self.repos = repos or []
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Dict:
        """
        Make authenticated request to GitHub API.
        
        Args:
            url: API endpoint URL
            params: Optional query parameters
            
        Returns:
            JSON response as dictionary
        """
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GitHub API request failed: {e}")
            return {}
    
    def get_user_created_prs(self) -> List[Dict]:
        """
        Get all open PRs created by the user.
        
        Returns:
            List of PR dictionaries
        """
        query = f"is:pr is:open author:{self.username}"
        
        # Add org filter if specified
        if self.org:
            query += f" org:{self.org}"
        
        # Add repo filter if specified
        if self.repos:
            repo_query = " ".join([f"repo:{self.org}/{repo}" for repo in self.repos])
            query = f"is:pr is:open author:{self.username} {repo_query}"
        
        url = f"{self.base_url}/search/issues"
        params = {
            "q": query,
            "sort": "created",
            "order": "desc",
            "per_page": 50
        }
        
        result = self._make_request(url, params)
        return result.get("items", [])
    
    def get_prs_awaiting_review(self) -> List[Dict]:
        """
        Get all open PRs where the user is requested as a reviewer.
        
        Returns:
            List of PR dictionaries
        """
        query = f"is:pr is:open review-requested:{self.username}"
        
        # Add org filter if specified
        if self.org:
            query += f" org:{self.org}"
        
        # Add repo filter if specified
        if self.repos:
            repo_query = " ".join([f"repo:{self.org}/{repo}" for repo in self.repos])
            query = f"is:pr is:open review-requested:{self.username} {repo_query}"
        
        url = f"{self.base_url}/search/issues"
        params = {
            "q": query,
            "sort": "created",
            "order": "desc",
            "per_page": 50
        }
        
        result = self._make_request(url, params)
        return result.get("items", [])
    
    def get_assigned_prs(self) -> List[Dict]:
        """
        Get all open PRs assigned to the user.
        
        Returns:
            List of PR dictionaries
        """
        query = f"is:pr is:open assignee:{self.username}"
        
        # Add org filter if specified
        if self.org:
            query += f" org:{self.org}"
        
        # Add repo filter if specified
        if self.repos:
            repo_query = " ".join([f"repo:{self.org}/{repo}" for repo in self.repos])
            query = f"is:pr is:open assignee:{self.username} {repo_query}"
        
        url = f"{self.base_url}/search/issues"
        params = {
            "q": query,
            "sort": "created",
            "order": "desc",
            "per_page": 50
        }
        
        result = self._make_request(url, params)
        return result.get("items", [])
    
    def get_prs_with_failed_ci(self) -> List[Dict]:
        """
        Get PRs created by user where CI has failed (optional feature).
        
        Returns:
            List of PR dictionaries with failed CI
        """
        query = f"is:pr is:open author:{self.username} status:failure"
        
        # Add org filter if specified
        if self.org:
            query += f" org:{self.org}"
        
        # Add repo filter if specified
        if self.repos:
            repo_query = " ".join([f"repo:{self.org}/{repo}" for repo in self.repos])
            query = f"is:pr is:open author:{self.username} status:failure {repo_query}"
        
        url = f"{self.base_url}/search/issues"
        params = {
            "q": query,
            "sort": "created",
            "order": "desc",
            "per_page": 50
        }
        
        result = self._make_request(url, params)
        return result.get("items", [])
    
    def get_all_user_work(self) -> Dict[str, List[Dict]]:
        """
        Get all GitHub work for the user.
        
        Returns:
            Dictionary with categorized PRs
        """
        return {
            "created": self.get_user_created_prs(),
            "review_requested": self.get_prs_awaiting_review(),
            "assigned": self.get_assigned_prs(),
            "failed_ci": self.get_prs_with_failed_ci()
        }


def create_github_client() -> Optional[GitHubClient]:
    """
    Create GitHub client from environment variables.
    
    Returns:
        GitHubClient instance or None if config is missing
    """
    token = os.getenv("GITHUB_TOKEN")
    org = os.getenv("GITHUB_ORG")
    username = os.getenv("GITHUB_USERNAME")
    repos_str = os.getenv("GITHUB_REPOS", "")
    
    if not token or not username:
        print("GitHub configuration missing: GITHUB_TOKEN and GITHUB_USERNAME are required")
        return None
    
    repos = [r.strip() for r in repos_str.split(",") if r.strip()] if repos_str else []
    
    return GitHubClient(token=token, org=org, username=username, repos=repos)

