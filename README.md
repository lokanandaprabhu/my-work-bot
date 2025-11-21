# 🤖 My Work Bot

A Slack bot that helps developers quickly see all their pending work across GitHub, Jira, and personal todos with a single command.

## ✨ Features

- **Single Command**: Type `/mywork` in Slack to get a complete overview of ALL your work
- **GitHub Integration**:
  - PRs you created that are still open
  - PRs waiting for your review
  - PRs assigned to you
  - PRs with failed CI checks (optional)
- **Jira Integration**:
  - Issues assigned to you
  - Categorized by status (To Do, In Progress, Blocked)
  - Shows priority, summary, and direct links
- **Personal TODO List** ✨ NEW!:
  - Add, edit, and track your personal todos
  - Mark todos as complete
  - View todos alongside your GitHub and Jira work
  - Persistent storage per user
- **Beautiful Formatting**: Uses Slack Block Kit for a modern, readable interface

## 📁 Project Structure

```
my-work-bot/
├── src/
│   ├── __init__.py
│   ├── app.py                 # Main application entry point
│   ├── slack/
│   │   ├── __init__.py
│   │   └── bot.py             # Slack bot implementation
│   ├── github/
│   │   ├── __init__.py
│   │   └── client.py          # GitHub API client
│   ├── jira/
│   │   ├── __init__.py
│   │   └── client.py          # Jira API client
│   ├── storage/               # NEW: TODO storage
│   │   ├── __init__.py
│   │   └── todo_store.py      # Personal TODO management
│   └── utils/
│       ├── __init__.py
│       └── formatter.py       # Slack message formatter
├── data/                       # NEW: TODO data storage
│   └── todos.json             # User todos (auto-created)
├── run.py                      # Convenience runner script
├── start_bot.sh               # Quick start script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- A Slack workspace where you can install apps
- GitHub personal access token
- Jira API token

### 1. Clone the Repository

```bash
cd my-work-bot
```

### 2. Install Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 3. Set Up Slack App

#### Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. Name it "My Work Bot" and select your workspace

#### Configure Bot Token Scopes

1. Navigate to **OAuth & Permissions**
2. Under **Bot Token Scopes**, add:
   - `commands` - For slash commands
   - `chat:write` - To send messages
   - `app_mentions:read` - To respond to @mentions

#### Create Slash Command

1. Navigate to **Slash Commands**
2. Click **"Create New Command"**
3. Set:
   - **Command**: `/mywork`
   - **Request URL**: `https://your-domain.com/slack/events` (or use ngrok for local dev)
   - **Short Description**: "View your pending work from GitHub and Jira"
   - **Usage Hint**: (leave empty)

#### Enable Socket Mode (For Local Development)

1. Navigate to **Socket Mode**
2. Enable Socket Mode
3. Generate an app-level token with `connections:write` scope
4. Save this as `SLACK_APP_TOKEN`

#### Install App to Workspace

1. Navigate to **Install App**
2. Click **"Install to Workspace"**
3. Authorize the app
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### 4. Set Up GitHub

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Click **"Generate new token (classic)"**
3. Select scopes:
   - `repo` - Full control of private repositories
   - `read:org` - Read org and team membership
4. Generate and copy the token

### 5. Set Up Jira

1. Go to [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **"Create API token"**
3. Give it a label (e.g., "My Work Bot")
4. Copy the token

### 6. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_SIGNING_SECRET=your-signing-secret-here
SLACK_APP_TOKEN=xapp-your-app-token-here
SLASH_COMMAND=/mywork

# GitHub Configuration
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_ORG=your-organization-name
GITHUB_USERNAME=your-github-username
GITHUB_REPOS=repo1,repo2,repo3  # Optional: leave empty to check all repos

# Jira Configuration
JIRA_EMAIL=your-email@company.com
JIRA_API_TOKEN=your-jira-api-token-here
JIRA_BASE_URL=https://your-company.atlassian.net
```

### 7. Run the Bot

```bash
python run.py
```

You should see:

```
==================================================
🤖 Starting My Work Bot for Developer Week
==================================================
✅ GitHub integration enabled
✅ Jira integration enabled

==================================================
⚡️ Bot is running in Socket Mode with command: /mywork
```

### 8. Test the Bot

1. Open Slack
2. Type `/mywork` in any channel
3. The bot will fetch and display your pending work!
4. Try the TODO commands:
   - `/todo add Prepare for Developer Week`
   - `/todo list`
   - `/mywork` (see todos alongside GitHub and Jira!)

## 📝 Personal TODO Commands

The bot includes a personal TODO list feature to help you track tasks that don't belong in GitHub or Jira:

### Available Commands

```
/todo                           # Show help
/todo add <description>         # Add a new todo
/todo list                      # Show all your todos
/todo done <id>                 # Mark a todo as complete
/todo delete <id>              # Delete a todo
/todo edit <id> <description>  # Edit a todo
```

### Examples

```
/todo add Review PR #123 by EOD
/todo add Update documentation for new API
/todo done 3
/todo edit 1 Review PR #123 AND merge if approved
/todo list
```

Your todos are stored locally in `data/todos.json` and are never shared with other users.

## 🔧 Configuration Options

### Environment Variables

| Variable               | Required | Description                                |
| ---------------------- | -------- | ------------------------------------------ |
| `SLACK_BOT_TOKEN`      | Yes      | Bot user OAuth token from Slack            |
| `SLACK_SIGNING_SECRET` | Yes      | Signing secret from Slack app settings     |
| `SLACK_APP_TOKEN`      | No\*     | App-level token (required for Socket Mode) |
| `SLASH_COMMAND`        | No       | Custom slash command (default: `/mywork`)  |
| `GITHUB_TOKEN`         | No\*\*   | GitHub personal access token               |
| `GITHUB_ORG`           | No       | GitHub organization to filter              |
| `GITHUB_USERNAME`      | No\*\*   | Your GitHub username                       |
| `GITHUB_REPOS`         | No       | Comma-separated list of repos to monitor   |
| `JIRA_EMAIL`           | No\*\*   | Your Jira account email                    |
| `JIRA_API_TOKEN`       | No\*\*   | Jira API token                             |
| `JIRA_BASE_URL`        | No\*\*   | Your Jira instance URL                     |
