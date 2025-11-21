# ⚡ Quick Start Guide

Get your My Work Bot up and running in 10 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Slack workspace with admin access
- [ ] GitHub account with personal access token
- [ ] Jira account with API access

## 5-Minute Setup

### Step 1: Install Dependencies (1 min)

```bash
cd my-work-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 2: Create Slack App (3 min)

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"** → **"From scratch"**
3. Name: "My Work Bot", select your workspace
4. Go to **OAuth & Permissions** → Add scopes:
   - `commands`
   - `chat:write`
   - `app_mentions:read`
5. Go to **Socket Mode** → Enable → Create token with `connections:write`
6. Go to **Slash Commands** → Create `/mywork`
7. **Install App** → Copy **Bot User OAuth Token**

### Step 3: Get API Tokens (3 min)

**GitHub:**
1. [github.com/settings/tokens](https://github.com/settings/tokens)
2. Generate token with `repo` and `read:org` scopes

**Jira:**
1. [id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Create API token

### Step 4: Configure Environment (2 min)

Create `.env` file:

```bash
# Slack
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_SIGNING_SECRET=your-secret
SLACK_APP_TOKEN=xapp-your-token

# GitHub
GITHUB_TOKEN=ghp_your-token
GITHUB_USERNAME=your-username
GITHUB_ORG=your-org

# Jira
JIRA_EMAIL=you@company.com
JIRA_API_TOKEN=your-token
JIRA_BASE_URL=https://company.atlassian.net
```

### Step 5: Run! (1 min)

```bash
python run.py
```

You should see:
```
⚡️ Bot is running in Socket Mode with command: /mywork
```

### Step 6: Test

Open Slack and type `/mywork` 🎉

## Troubleshooting

### "SLACK_BOT_TOKEN is required"
→ Check your `.env` file has the correct variable names

### "GitHub API request failed"
→ Verify your GitHub token has the right scopes

### "Jira API request failed"
→ Check your Jira base URL includes `https://`

### Bot doesn't respond
→ Ensure Socket Mode is enabled in Slack app settings

## Next Steps

- 📖 Read [README.md](README.md) for complete documentation
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- 👀 See [SAMPLE_OUTPUT.md](SAMPLE_OUTPUT.md) for example responses
- 🤝 Read [CONTRIBUTING.md](CONTRIBUTING.md) to add features

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run bot
python run.py

# Install new dependency
pip install package-name
pip freeze > requirements.txt

# Deactivate virtual environment
deactivate
```

## Pro Tips

1. **Start with one integration**: Get GitHub OR Jira working first
2. **Use Socket Mode locally**: No need for ngrok/public URL
3. **Check logs**: The bot prints helpful error messages
4. **Test incrementally**: Add one feature at a time

## Support

- 📄 Full docs: [README.md](README.md)
- 🐛 Found a bug? Open an issue
- 💡 Have an idea? Check [CONTRIBUTING.md](CONTRIBUTING.md)

---

**You're all set!** Type `/mywork` in Slack to see your pending work. 🚀

