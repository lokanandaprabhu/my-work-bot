"""
Slack Bot implementation using Bolt framework.
"""
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from typing import Optional

from github.client import create_github_client
from jira.client import create_jira_client
from utils.formatter import SlackMessageFormatter
from storage.todo_store import get_todo_store


class MyWorkBot:
    """Slack bot that handles the /mywork command."""
    
    def __init__(self):
        """Initialize the Slack bot."""
        # Get environment variables
        self.bot_token = os.getenv("SLACK_BOT_TOKEN")
        self.signing_secret = os.getenv("SLACK_SIGNING_SECRET")
        self.app_token = os.getenv("SLACK_APP_TOKEN")
        self.slash_command = os.getenv("SLASH_COMMAND", "/mywork")
        
        if not self.bot_token or not self.signing_secret:
            raise ValueError("SLACK_BOT_TOKEN and SLACK_SIGNING_SECRET are required")
        
        # Initialize Slack app
        self.app = App(
            token=self.bot_token,
            signing_secret=self.signing_secret
        )
        
        # Initialize API clients
        self.github_client = create_github_client()
        self.jira_client = create_jira_client()
        self.todo_store = get_todo_store()
        
        # Register command handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register Slack command handlers."""
        
        @self.app.command(self.slash_command)
        def handle_mywork_command(ack, respond, command):
            """Handle /mywork slash command."""
            # Acknowledge the command immediately
            ack()
            
            try:
                # Send loading message
                respond(blocks=SlackMessageFormatter.create_loading_message())
                
                # Get user ID
                user_id = command.get("user_id")
                
                # Fetch data from GitHub, Jira, and Todos
                github_data = self._fetch_github_data()
                jira_data = self._fetch_jira_data()
                todos = self.todo_store.get_todos(user_id, include_completed=True)
                
                # Format the response
                blocks = SlackMessageFormatter.create_my_work_message(
                    github_data=github_data,
                    jira_data=jira_data,
                    todos=todos
                )
                
                # Send the formatted response
                respond(
                    blocks=blocks,
                    replace_original=True
                )
                
            except Exception as e:
                error_msg = f"Sorry, something went wrong: {str(e)}"
                respond(
                    blocks=SlackMessageFormatter.create_error_message(error_msg),
                    replace_original=True
                )
        
        @self.app.command("/todo")
        def handle_todo_command(ack, respond, command):
            """Handle /todo slash command with subcommands."""
            ack()
            
            user_id = command.get("user_id")
            text = command.get("text", "").strip()
            
            try:
                # Parse subcommand
                if not text:
                    # Show help
                    self._show_todo_help(respond)
                elif text.startswith("add "):
                    # Add todo
                    description = text[4:].strip()
                    if not description:
                        respond("❌ Please provide a description.\nUsage: `/todo add <description>`")
                        return
                    
                    todo = self.todo_store.add_todo(user_id, description)
                    respond(f"✅ Added todo #{todo['id']}: {description}")
                
                elif text == "list":
                    # List todos
                    self._show_todo_list(user_id, respond)
                
                elif text.startswith("done "):
                    # Mark todo as done
                    try:
                        todo_id = int(text[5:].strip())
                        todo = self.todo_store.complete_todo(user_id, todo_id)
                        if todo:
                            respond(f"✅ Completed todo #{todo_id}: ~{todo['description']}~")
                        else:
                            respond(f"❌ Todo #{todo_id} not found.")
                    except ValueError:
                        respond("❌ Invalid todo ID.\nUsage: `/todo done <id>`")
                
                elif text.startswith("delete "):
                    # Delete todo
                    try:
                        todo_id = int(text[7:].strip())
                        if self.todo_store.delete_todo(user_id, todo_id):
                            respond(f"🗑️ Deleted todo #{todo_id}")
                        else:
                            respond(f"❌ Todo #{todo_id} not found.")
                    except ValueError:
                        respond("❌ Invalid todo ID.\nUsage: `/todo delete <id>`")
                
                elif text.startswith("edit "):
                    # Edit todo
                    parts = text[5:].strip().split(" ", 1)
                    if len(parts) != 2:
                        respond("❌ Usage: `/todo edit <id> <new description>`")
                        return
                    
                    try:
                        todo_id = int(parts[0])
                        new_description = parts[1].strip()
                        todo = self.todo_store.update_todo(user_id, todo_id, new_description)
                        if todo:
                            respond(f"✏️ Updated todo #{todo_id}: {new_description}")
                        else:
                            respond(f"❌ Todo #{todo_id} not found.")
                    except ValueError:
                        respond("❌ Invalid todo ID.\nUsage: `/todo edit <id> <new description>`")
                
                else:
                    # Unknown subcommand
                    respond(f"❌ Unknown command: `{text.split()[0]}`\n\nUse `/todo` to see available commands.")
                    
            except Exception as e:
                respond(f"❌ Error: {str(e)}")
        
        @self.app.event("app_mention")
        def handle_app_mention(event, say):
            """Handle @bot mentions."""
            user = event.get("user")
            say(f"Hi <@{user}>! 👋\n\nUse `{self.slash_command}` to see your pending work from GitHub and Jira.\nUse `/todo` to manage your personal todos.")
        
        @self.app.event("message")
        def handle_message_events(body, logger):
            """Handle message events (required for socket mode)."""
            logger.debug(body)
    
    def _fetch_github_data(self) -> dict:
        """
        Fetch GitHub data.
        
        Returns:
            Dictionary with GitHub PR data
        """
        if not self.github_client:
            return {
                "created": [],
                "review_requested": [],
                "assigned": [],
                "failed_ci": []
            }
        
        try:
            return self.github_client.get_all_user_work()
        except Exception as e:
            print(f"Error fetching GitHub data: {e}")
            return {
                "created": [],
                "review_requested": [],
                "assigned": [],
                "failed_ci": []
            }
    
    def _fetch_jira_data(self) -> dict:
        """
        Fetch Jira data.
        
        Returns:
            Dictionary with Jira issue data
        """
        if not self.jira_client:
            return {
                "all_issues": [],
                "categorized": {
                    "todo": [],
                    "in_progress": [],
                    "blocked": [],
                    "other": []
                }
            }
        
        try:
            return self.jira_client.get_all_user_work()
        except Exception as e:
            print(f"Error fetching Jira data: {e}")
            return {
                "all_issues": [],
                "categorized": {
                    "todo": [],
                    "in_progress": [],
                    "blocked": [],
                    "other": []
                }
            }
    
    def _show_todo_help(self, respond):
        """Show TODO command help."""
        help_text = """
*📝 Personal TODO Commands*

• `/todo add <description>` - Add a new todo
• `/todo list` - Show all your todos
• `/todo done <id>` - Mark a todo as complete
• `/todo delete <id>` - Remove a todo
• `/todo edit <id> <new description>` - Edit a todo

*Examples:*
• `/todo add Review PR #123 by EOD`
• `/todo done 3`
• `/todo edit 1 Updated task description`

Your todos will appear in `/mywork` along with GitHub and Jira!
        """
        respond(help_text.strip())
    
    def _show_todo_list(self, user_id: str, respond):
        """Show user's todo list."""
        todos = self.todo_store.get_todos(user_id, include_completed=True)
        
        if not todos:
            respond("✨ You have no todos! Add one with `/todo add <description>`")
            return
        
        # Separate active and completed
        active_todos = [t for t in todos if not t.get("completed", False)]
        completed_todos = [t for t in todos if t.get("completed", False)]
        
        response = "*📝 Your Todos*\n\n"
        
        if active_todos:
            response += "*Active:*\n"
            for todo in active_todos:
                todo_id = todo.get("id")
                description = todo.get("description")
                priority = todo.get("priority", "medium")
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                response += f"{priority_emoji} ⬜ *{todo_id}.* {description}\n"
            response += "\n"
        
        if completed_todos:
            response += "*Completed:*\n"
            for todo in completed_todos[-5:]:  # Show last 5
                todo_id = todo.get("id")
                description = todo.get("description")
                response += f"✅ ~{todo_id}. {description}~\n"
        
        stats = self.todo_store.get_stats(user_id)
        response += f"\n_{stats['active']} active, {stats['completed']} completed_"
        
        respond(response)
    
    def start(self):
        """Start the bot."""
        if self.app_token:
            # Use Socket Mode (for local development)
            print(f"⚡️ Bot is running in Socket Mode")
            print(f"   Commands: {self.slash_command}, /todo")
            handler = SocketModeHandler(self.app, self.app_token)
            handler.start()
        else:
            # Use HTTP mode (for production)
            print(f"⚡️ Bot is running in HTTP Mode")
            print(f"   Commands: {self.slash_command}, /todo")
            self.app.start(port=int(os.environ.get("PORT", 3000)))


def create_bot() -> MyWorkBot:
    """
    Create and return a MyWorkBot instance.
    
    Returns:
        MyWorkBot instance
    """
    return MyWorkBot()

