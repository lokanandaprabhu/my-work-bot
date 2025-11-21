#!/usr/bin/env python3
"""
Demo script to test /mywork functionality without Slack.
This shows exactly what the bot will display in Slack.
"""
from dotenv import load_dotenv
load_dotenv()

from src.github.client import create_github_client
from src.jira.client import create_jira_client
from src.utils.formatter import SlackMessageFormatter

def print_separator(char="=", length=70):
    print(char * length)

def print_header(text):
    print_separator()
    print(f"  {text}")
    print_separator()

def convert_blocks_to_text(blocks):
    """Convert Slack blocks to readable text."""
    for block in blocks:
        block_type = block.get("type")
        
        if block_type == "header":
            text = block.get("text", {}).get("text", "")
            print(f"\n{text}")
            print("=" * len(text))
        
        elif block_type == "section":
            text = block.get("text", {}).get("text", "")
            # Clean up markdown for terminal
            text = text.replace("*", "")
            text = text.replace("_", "")
            # Handle links: <url|text> -> text (url)
            import re
            text = re.sub(r'<([^|>]+)\|([^>]+)>', r'\2 (\1)', text)
            text = re.sub(r'<([^>]+)>', r'\1', text)
            print(text)
        
        elif block_type == "divider":
            print("\n" + "-" * 70)
        
        elif block_type == "context":
            elements = block.get("elements", [])
            for elem in elements:
                text = elem.get("text", "")
                text = text.replace("*", "")
                text = text.replace("_", "")
                print(f"\n{text}")

def main():
    print_header("🤖 MY WORK BOT - DEMO (No Slack Required)")
    
    print("\n📊 Current Configuration:")
    print("  ✅ GitHub: ENABLED")
    print("  ⏸️  Jira: DISABLED (focusing on GitHub + Slack)")
    print("  ⏳ Slack: Waiting for sandbox access")
    
    print("\n🔍 Fetching your work from GitHub...")
    
    # Fetch GitHub data
    github_client = create_github_client()
    if not github_client:
        print("\n❌ Error: Could not create GitHub client")
        print("   Check your GITHUB_TOKEN in .env file")
        return
    
    print("  ✓ GitHub client created")
    github_data = github_client.get_all_user_work()
    
    print(f"  ✓ Found {len(github_data['created'])} PRs you created")
    print(f"  ✓ Found {len(github_data['review_requested'])} PRs waiting for your review")
    print(f"  ✓ Found {len(github_data['assigned'])} PRs assigned to you")
    print(f"  ✓ Found {len(github_data['failed_ci'])} PRs with failed CI")
    
    # Jira data (empty for now)
    jira_data = {
        "all_issues": [],
        "categorized": {
            "todo": [],
            "in_progress": [],
            "blocked": [],
            "other": []
        }
    }
    
    # Generate Slack message blocks
    blocks = SlackMessageFormatter.create_my_work_message(github_data, jira_data)
    
    # Display as text
    print("\n")
    print_separator("═")
    print("  📱 SLACK MESSAGE PREVIEW")
    print("  (This is what users will see when they type /mywork)")
    print_separator("═")
    
    convert_blocks_to_text(blocks)
    
    print("\n")
    print_separator()
    print("✨ Bot is ready! Just need Slack credentials to go live.")
    print_separator()
    
    print("\n📋 Next Steps:")
    print("  1. Get Stage SSO access (https://auth.stage.redhat.com)")
    print("  2. Access sandbox (https://redhat-sandbox.enterprise.slack.com)")
    print("  3. Create Slack app in sandbox")
    print("  4. Add tokens to .env")
    print("  5. Run: python run.py")
    print("\n")

if __name__ == "__main__":
    main()

