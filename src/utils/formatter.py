"""
Slack message formatter using Block Kit.
"""
from typing import List, Dict, Any


class SlackMessageFormatter:
    """Formatter for creating beautiful Slack Block Kit messages."""
    
    @staticmethod
    def create_header(text: str, emoji: str = "📋") -> Dict:
        """Create a header block."""
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{emoji} {text}",
                "emoji": True
            }
        }
    
    @staticmethod
    def create_divider() -> Dict:
        """Create a divider block."""
        return {"type": "divider"}
    
    @staticmethod
    def create_section(text: str, markdown: bool = True) -> Dict:
        """Create a section block with text."""
        return {
            "type": "section",
            "text": {
                "type": "mrkdwn" if markdown else "plain_text",
                "text": text
            }
        }
    
    @staticmethod
    def create_context(elements: List[str]) -> Dict:
        """Create a context block with multiple text elements."""
        return {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": element
                }
                for element in elements
            ]
        }
    
    @staticmethod
    def format_github_prs(github_data: Dict[str, List[Dict]]) -> List[Dict]:
        """
        Format GitHub PR data into Slack blocks.
        
        Args:
            github_data: Dictionary containing categorized PRs
            
        Returns:
            List of Slack blocks
        """
        blocks = []
        
        # Header
        blocks.append(SlackMessageFormatter.create_section("*🐙 GitHub Pull Requests*"))
        
        has_any_prs = False
        
        # PRs created by user
        created_prs = github_data.get("created", [])
        if created_prs:
            has_any_prs = True
            blocks.append(SlackMessageFormatter.create_section("*Your Open PRs* 📝"))
            for pr in created_prs[:10]:  # Limit to 10
                repo_name = pr.get("repository_url", "").split("/")[-1] if pr.get("repository_url") else "repo"
                pr_title = pr.get("title", "Untitled PR")
                pr_url = pr.get("html_url", "#")
                pr_number = pr.get("number", "?")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"• <{pr_url}|#{pr_number}: {pr_title}>\n   `{repo_name}`"
                    )
                )
        
        # PRs awaiting review
        review_prs = github_data.get("review_requested", [])
        if review_prs:
            has_any_prs = True
            blocks.append(SlackMessageFormatter.create_divider())
            blocks.append(SlackMessageFormatter.create_section("*Waiting for Your Review* 👀"))
            for pr in review_prs[:10]:  # Limit to 10
                repo_name = pr.get("repository_url", "").split("/")[-1] if pr.get("repository_url") else "repo"
                pr_title = pr.get("title", "Untitled PR")
                pr_url = pr.get("html_url", "#")
                pr_number = pr.get("number", "?")
                author = pr.get("user", {}).get("login", "unknown")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"• <{pr_url}|#{pr_number}: {pr_title}>\n   `{repo_name}` by @{author}"
                    )
                )
        
        # Assigned PRs
        assigned_prs = github_data.get("assigned", [])
        if assigned_prs:
            has_any_prs = True
            blocks.append(SlackMessageFormatter.create_divider())
            blocks.append(SlackMessageFormatter.create_section("*Assigned to You* 👤"))
            for pr in assigned_prs[:10]:  # Limit to 10
                repo_name = pr.get("repository_url", "").split("/")[-1] if pr.get("repository_url") else "repo"
                pr_title = pr.get("title", "Untitled PR")
                pr_url = pr.get("html_url", "#")
                pr_number = pr.get("number", "?")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"• <{pr_url}|#{pr_number}: {pr_title}>\n   `{repo_name}`"
                    )
                )
        
        # Failed CI (optional)
        failed_ci_prs = github_data.get("failed_ci", [])
        if failed_ci_prs:
            has_any_prs = True
            blocks.append(SlackMessageFormatter.create_divider())
            blocks.append(SlackMessageFormatter.create_section("*Failed CI Checks* ⚠️"))
            for pr in failed_ci_prs[:5]:  # Limit to 5
                repo_name = pr.get("repository_url", "").split("/")[-1] if pr.get("repository_url") else "repo"
                pr_title = pr.get("title", "Untitled PR")
                pr_url = pr.get("html_url", "#")
                pr_number = pr.get("number", "?")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"• <{pr_url}|#{pr_number}: {pr_title}>\n   `{repo_name}`"
                    )
                )
        
        # If no PRs at all
        if not has_any_prs:
            blocks.append(
                SlackMessageFormatter.create_section("✨ _All clear! No pending PRs._")
            )
        
        return blocks
    
    @staticmethod
    def format_jira_issues(jira_data: Dict[str, Any]) -> List[Dict]:
        """
        Format Jira issue data into Slack blocks.
        
        Args:
            jira_data: Dictionary containing categorized issues
            
        Returns:
            List of Slack blocks
        """
        blocks = []
        
        # Header
        blocks.append(SlackMessageFormatter.create_section("*📊 Jira Issues*"))
        
        all_issues = jira_data.get("all_issues", [])
        
        if not all_issues:
            blocks.append(
                SlackMessageFormatter.create_section("✨ _All clear! No assigned issues._")
            )
            return blocks
        
        categorized = jira_data.get("categorized", {})
        
        # To Do issues
        todo_issues = categorized.get("todo", [])
        if todo_issues:
            blocks.append(SlackMessageFormatter.create_section("*To Do* 📝"))
            for issue in todo_issues[:10]:
                priority_emoji = {
                    "Highest": "🔴",
                    "High": "🟠",
                    "Medium": "🟡",
                    "Low": "🟢",
                    "Lowest": "⚪"
                }.get(issue.get("priority", ""), "⚪")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"{priority_emoji} <{issue['url']}|{issue['key']}> {issue['summary']}\n"
                        f"   _{issue['type']} • {issue['status']}_"
                    )
                )
        
        # In Progress issues
        in_progress_issues = categorized.get("in_progress", [])
        if in_progress_issues:
            blocks.append(SlackMessageFormatter.create_divider())
            blocks.append(SlackMessageFormatter.create_section("*In Progress* 🚀"))
            for issue in in_progress_issues[:10]:
                priority_emoji = {
                    "Highest": "🔴",
                    "High": "🟠",
                    "Medium": "🟡",
                    "Low": "🟢",
                    "Lowest": "⚪"
                }.get(issue.get("priority", ""), "⚪")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"{priority_emoji} <{issue['url']}|{issue['key']}> {issue['summary']}\n"
                        f"   _{issue['type']} • {issue['status']}_"
                    )
                )
        
        # Blocked issues
        blocked_issues = categorized.get("blocked", [])
        if blocked_issues:
            blocks.append(SlackMessageFormatter.create_divider())
            blocks.append(SlackMessageFormatter.create_section("*Blocked* 🚫"))
            for issue in blocked_issues[:10]:
                priority_emoji = {
                    "Highest": "🔴",
                    "High": "🟠",
                    "Medium": "🟡",
                    "Low": "🟢",
                    "Lowest": "⚪"
                }.get(issue.get("priority", ""), "⚪")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"{priority_emoji} <{issue['url']}|{issue['key']}> {issue['summary']}\n"
                        f"   _{issue['type']} • {issue['status']}_"
                    )
                )
        
        # Other issues
        other_issues = categorized.get("other", [])
        if other_issues:
            blocks.append(SlackMessageFormatter.create_divider())
            blocks.append(SlackMessageFormatter.create_section("*Other* 📌"))
            for issue in other_issues[:5]:
                priority_emoji = {
                    "Highest": "🔴",
                    "High": "🟠",
                    "Medium": "🟡",
                    "Low": "🟢",
                    "Lowest": "⚪"
                }.get(issue.get("priority", ""), "⚪")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"{priority_emoji} <{issue['url']}|{issue['key']}> {issue['summary']}\n"
                        f"   _{issue['type']} • {issue['status']}_"
                    )
                )
        
        return blocks
    
    @staticmethod
    def format_todos(todos: List[Dict]) -> List[Dict]:
        """
        Format personal todos into Slack blocks.
        
        Args:
            todos: List of todo dictionaries
            
        Returns:
            List of Slack blocks
        """
        blocks = []
        
        # Header
        blocks.append(SlackMessageFormatter.create_section("*✅ Personal Todos*"))
        
        if not todos:
            blocks.append(
                SlackMessageFormatter.create_section("✨ _No todos! Add one with `/todo add <description>`_")
            )
            return blocks
        
        # Separate active and completed
        active_todos = [t for t in todos if not t.get("completed", False)]
        completed_todos = [t for t in todos if t.get("completed", False)]
        
        # Show active todos
        if active_todos:
            for todo in active_todos[:10]:  # Limit to 10
                todo_id = todo.get("id", 0)
                description = todo.get("description", "No description")
                priority = todo.get("priority", "medium")
                
                # Priority emoji
                priority_emoji = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🟢"
                }.get(priority.lower(), "⚪")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"{priority_emoji} ⬜ *{todo_id}.* {description}"
                    )
                )
        
        # Show recently completed (last 3)
        if completed_todos:
            blocks.append(SlackMessageFormatter.create_section("\n_Recently completed:_"))
            for todo in completed_todos[-3:]:
                todo_id = todo.get("id", 0)
                description = todo.get("description", "No description")
                
                blocks.append(
                    SlackMessageFormatter.create_section(
                        f"✅ ~{todo_id}. {description}~"
                    )
                )
        
        # Add helper text
        blocks.append(
            SlackMessageFormatter.create_context([
                "_Manage todos: `/todo add`, `/todo done <id>`, `/todo list`_"
            ])
        )
        
        return blocks
    
    @staticmethod
    def create_my_work_message(github_data: Dict, jira_data: Dict, todos: List[Dict] = None) -> List[Dict]:
        """
        Create a complete /mywork response message.
        
        Args:
            github_data: GitHub PR data
            jira_data: Jira issue data
            todos: Personal todos list
            
        Returns:
            Complete list of Slack blocks
        """
        blocks = []
        
        # Main header
        blocks.append(SlackMessageFormatter.create_header("Your Pending Work", "📋"))
        blocks.append(SlackMessageFormatter.create_divider())
        
        # GitHub section
        github_blocks = SlackMessageFormatter.format_github_prs(github_data)
        blocks.extend(github_blocks)
        
        blocks.append(SlackMessageFormatter.create_divider())
        
        # Jira section
        jira_blocks = SlackMessageFormatter.format_jira_issues(jira_data)
        blocks.extend(jira_blocks)
        
        # Personal Todos section
        if todos is not None:
            blocks.append(SlackMessageFormatter.create_divider())
            todo_blocks = SlackMessageFormatter.format_todos(todos)
            blocks.extend(todo_blocks)
        
        # Footer
        blocks.append(SlackMessageFormatter.create_divider())
        blocks.append(
            SlackMessageFormatter.create_context([
                "💡 _Use `/mywork` anytime to see your latest pending work_"
            ])
        )
        
        return blocks
    
    @staticmethod
    def create_error_message(error_msg: str) -> List[Dict]:
        """
        Create an error message.
        
        Args:
            error_msg: Error message text
            
        Returns:
            List of Slack blocks
        """
        return [
            SlackMessageFormatter.create_section(f"❌ *Error*\n{error_msg}")
        ]
    
    @staticmethod
    def create_loading_message() -> List[Dict]:
        """
        Create a loading message.
        
        Returns:
            List of Slack blocks
        """
        return [
            SlackMessageFormatter.create_section("⏳ _Fetching your work from GitHub, Jira, and Todos..._")
        ]

