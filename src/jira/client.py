"""
Jira API Client for fetching assigned issues.
"""
import os
import requests
from typing import List, Dict, Optional
import base64


class JiraClient:
    """Client to interact with Jira REST API."""
    
    def __init__(self, email: str, api_token: str, base_url: str):
        """
        Initialize Jira client.
        
        Args:
            email: Jira account email (can be username for Bearer auth)
            api_token: Jira API token (Personal Access Token)
            base_url: Jira instance base URL (e.g., https://issues.redhat.com)
        """
        self.email = email
        self.api_token = api_token
        self.base_url = base_url.rstrip("/")
        
        # Use Bearer token authentication (Red Hat Jira style)
        # Based on: https://github.com/openshift-dev-console/daily-status-bot
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make authenticated request to Jira API.
        
        Args:
            endpoint: API endpoint path
            params: Optional query parameters
            
        Returns:
            JSON response as dictionary
        """
        url = f"{self.base_url}/rest/api/2/{endpoint}"
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Jira API request failed: {e}")
            return {}
    
    def get_user_issues(self) -> List[Dict]:
        """
        Get all unresolved issues assigned to the current user.
        Uses JQL: assignee = currentUser() AND resolution = Unresolved
        
        Returns:
            List of issue dictionaries
        """
        jql = "assignee = currentUser() AND resolution = Unresolved ORDER BY priority DESC, updated DESC"
        
        params = {
            "jql": jql,
            "maxResults": 50,
            "fields": "summary,status,priority,assignee,issuetype,updated,created"
        }
        
        result = self._make_request("search", params)
        return result.get("issues", [])
    
    def get_issues_by_status(self, statuses: List[str]) -> List[Dict]:
        """
        Get user's issues filtered by specific statuses.
        
        Args:
            statuses: List of status names (e.g., ["To Do", "In Progress", "Blocked"])
            
        Returns:
            List of issue dictionaries
        """
        status_filter = ", ".join([f'"{status}"' for status in statuses])
        jql = f"assignee = currentUser() AND resolution = Unresolved AND status IN ({status_filter}) ORDER BY priority DESC, updated DESC"
        
        params = {
            "jql": jql,
            "maxResults": 50,
            "fields": "summary,status,priority,assignee,issuetype,updated,created"
        }
        
        result = self._make_request("search", params)
        return result.get("issues", [])
    
    def format_issue(self, issue: Dict) -> Dict:
        """
        Format a Jira issue into a simplified structure.
        
        Args:
            issue: Raw Jira issue dictionary
            
        Returns:
            Formatted issue dictionary
        """
        fields = issue.get("fields", {})
        issue_key = issue.get("key", "")
        
        return {
            "key": issue_key,
            "summary": fields.get("summary", "No summary"),
            "status": fields.get("status", {}).get("name", "Unknown"),
            "priority": fields.get("priority", {}).get("name", "None"),
            "type": fields.get("issuetype", {}).get("name", "Task"),
            "url": f"{self.base_url}/browse/{issue_key}",
            "updated": fields.get("updated", ""),
            "created": fields.get("created", "")
        }
    
    def get_all_user_work(self) -> Dict[str, List[Dict]]:
        """
        Get all Jira work for the user, categorized by status.
        
        Returns:
            Dictionary with categorized issues
        """
        # Get all unresolved issues
        all_issues = self.get_user_issues()
        
        # Categorize by status
        categorized = {
            "todo": [],
            "in_progress": [],
            "blocked": [],
            "other": []
        }
        
        for issue in all_issues:
            formatted_issue = self.format_issue(issue)
            status = formatted_issue["status"].lower()
            
            if "to do" in status or "todo" in status or "backlog" in status:
                categorized["todo"].append(formatted_issue)
            elif "in progress" in status or "in review" in status or "development" in status:
                categorized["in_progress"].append(formatted_issue)
            elif "blocked" in status or "waiting" in status or "hold" in status:
                categorized["blocked"].append(formatted_issue)
            else:
                categorized["other"].append(formatted_issue)
        
        return {
            "all_issues": [self.format_issue(issue) for issue in all_issues],
            "categorized": categorized
        }


def create_jira_client() -> Optional[JiraClient]:
    """
    Create Jira client from environment variables.
    
    Returns:
        JiraClient instance or None if config is missing
    """
    email = os.getenv("JIRA_EMAIL")
    api_token = os.getenv("JIRA_API_TOKEN")
    base_url = os.getenv("JIRA_BASE_URL")
    
    if not email or not api_token or not base_url:
        print("Jira configuration missing: JIRA_EMAIL, JIRA_API_TOKEN, and JIRA_BASE_URL are required")
        return None
    
    return JiraClient(email=email, api_token=api_token, base_url=base_url)

