# 🤖 My Work Bot - Developer Week Edition

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

### Features

- ✅ **User-Specific**: Each user has their own private todo list
- ✅ **Persistent**: Todos are saved and survive bot restarts
- ✅ **Integrated**: Todos appear in `/mywork` alongside GitHub and Jira
- ✅ **Priority Indicators**: High/medium/low priority with colored emojis
- ✅ **Completion Tracking**: Mark todos as done and see recently completed

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

\* Required for local development with Socket Mode  
\*\* Required if you want that integration to work

### Running Without GitHub or Jira

The bot will work with partial configuration:

- Without GitHub credentials: Only shows Jira issues
- Without Jira credentials: Only shows GitHub PRs
- Without both: Shows friendly "All clear!" messages

## 🌐 Deployment Options

### Option 1: Local Development with ngrok

```bash
# In one terminal, start the bot
python run.py

# The bot will run in Socket Mode (no ngrok needed for Socket Mode!)
```

### Option 2: Deploy to Heroku

```bash
# Install Heroku CLI and login
heroku login

# Create a new Heroku app
heroku create my-work-bot

# Set environment variables
heroku config:set SLACK_BOT_TOKEN=xoxb-...
heroku config:set SLACK_SIGNING_SECRET=...
# ... (set all other required vars)

# Create Procfile
echo "web: python run.py" > Procfile

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# For Heroku, remove SLACK_APP_TOKEN to use HTTP mode instead of Socket Mode
heroku config:unset SLACK_APP_TOKEN
```

### Option 3: Deploy to Render

1. Create a new Web Service on [render.com](https://render.com)
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python run.py`
5. Add all environment variables
6. Deploy!

### Option 4: Deploy to AWS Lambda

For serverless deployment, you'll need to adapt the bot to use AWS Lambda handlers. Consider using the `serverless-slack` framework.

### Option 5: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Add environment variables
4. Deploy automatically!

## 📱 Sample Output

When you type `/mywork`, you'll see something like this:

```
📋 Your Pending Work
━━━━━━━━━━━━━━━━━━━━━━━━━━

🐙 GitHub Pull Requests

Your Open PRs 📝
• #123: Add new feature for user authentication
   `backend-api`
• #124: Fix bug in payment processing
   `payment-service`

Waiting for Your Review 👀
• #125: Update documentation for API v2
   `docs` by @jane
• #126: Refactor database queries
   `backend-api` by @john

━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Jira Issues

To Do 📝
🔴 PROJ-123 Implement user authentication flow
   Story • To Do
🟡 PROJ-124 Update API documentation
   Task • To Do

In Progress 🚀
🟠 PROJ-125 Fix critical bug in checkout
   Bug • In Progress

━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 Use /mywork anytime to see your latest pending work
```

## 🛠️ Troubleshooting

### Bot doesn't respond to `/mywork`

1. Check that the slash command is created in Slack app settings
2. Verify the bot is running (`python run.py` should show no errors)
3. Ensure Socket Mode is enabled with a valid `SLACK_APP_TOKEN`
4. Check that the bot has the correct OAuth scopes

### GitHub PRs not showing

1. Verify `GITHUB_TOKEN` has the required scopes (`repo`, `read:org`)
2. Check that `GITHUB_USERNAME` matches your GitHub username exactly
3. Ensure the token hasn't expired
4. Check the console for any API error messages

### Jira issues not showing

1. Verify `JIRA_BASE_URL` is correct (e.g., `https://company.atlassian.net`)
2. Check that `JIRA_EMAIL` matches your Atlassian account
3. Ensure the API token is valid and hasn't been revoked
4. Verify you have assigned issues in Jira

### Socket Mode connection issues

1. Make sure `SLACK_APP_TOKEN` starts with `xapp-`
2. Verify Socket Mode is enabled in Slack app settings
3. Check your internet connection
4. Try regenerating the app-level token

## 🎯 Suggestions for Improvement

### Additional Features to Consider

1. **Scheduled Digests**

   - Send daily/weekly summaries automatically
   - Configure digest times per user
   - Add morning standup summary

2. **Smart Notifications**

   - Alert when PRs go stale (no activity in X days)
   - Notify when CI fails on your PRs
   - Remind about pending reviews

3. **Interactive Actions**

   - Add buttons to take actions (approve PR, transition Jira issue)
   - Quick filters (show only high priority, etc.)
   - Mark items as "handled" to hide temporarily

4. **Team View**

   - `/teamwork` command to see team's work
   - Dashboard for managers
   - Team metrics and velocity tracking

5. **Additional Integrations**

   - Linear, Asana, Trello support
   - GitLab, Bitbucket support
   - Calendar integration (meetings, deadlines)

6. **Analytics & Insights**

   - Track PR review time
   - Measure work in progress
   - Generate productivity reports

7. **Customization**

   - Per-user preferences for what to show
   - Custom JQL queries
   - Configurable priorities and filters

8. **Collaboration Features**
   - Share your work status with teammates
   - Team standup mode
   - Cross-reference related items

## 🤝 Contributing

This is a Developer Week project! Feel free to:

- Fork the repository
- Add new features
- Submit pull requests
- Report issues

## 📄 License

MIT License - feel free to use this for your own Developer Week projects!

## 🙏 Acknowledgments

Built with:

- [Slack Bolt for Python](https://slack.dev/bolt-python/)
- [GitHub REST API](https://docs.github.com/en/rest)
- [Jira REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)

---

**Happy Developer Week! 🚀**

For questions or support, reach out to your team or check the documentation for each integrated service.
