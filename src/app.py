"""
Main application entry point for My Work Bot.
"""
import os
from dotenv import load_dotenv
from slack.bot import create_bot


def main():
    """Main entry point for the application."""
    # Load environment variables from .env file
    load_dotenv()
    
    print("=" * 50)
    print("🤖 Starting My Work Bot for Developer Week")
    print("=" * 50)
    
    # Validate required environment variables
    required_vars = ["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file and ensure all required variables are set.")
        return
    
    # Check optional configurations
    if not os.getenv("GITHUB_TOKEN"):
        print("⚠️  Warning: GITHUB_TOKEN not set. GitHub integration will be disabled.")
    else:
        print("✅ GitHub integration enabled")
    
    if not os.getenv("JIRA_API_TOKEN"):
        print("⚠️  Warning: JIRA_API_TOKEN not set. Jira integration will be disabled.")
    else:
        print("✅ Jira integration enabled")
    
    # Create and start the bot
    try:
        bot = create_bot()
        print("\n" + "=" * 50)
        bot.start()
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        raise


if __name__ == "__main__":
    main()

