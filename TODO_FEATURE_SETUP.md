# 📝 TODO Feature - Setup Guide

## Quick Setup for Slack

To enable the `/todo` command in your Slack workspace:

### 1. Add the Slash Command

1. Go to your Slack App settings: https://api.slack.com/apps
2. Select "My Work Bot"
3. Navigate to **"Slash Commands"**
4. Click **"Create New Command"**
5. Fill in:
   - **Command**: `/todo`
   - **Request URL**: Same as `/mywork` (Socket Mode handles routing)
   - **Short Description**: `Manage your personal todos`
   - **Usage Hint**: `add <description> | list | done <id> | delete <id>`
6. Click **"Save"**
7. **Reinstall your app** to workspace (required for new commands)

### 2. Test the Commands

In Slack, try:
```
/todo
```
You should see the help message with all available commands.

```
/todo add Prepare for Developer Week
```
You should get: ✅ Added todo #1: Prepare for Developer Week

```
/mywork
```
You should see your new todo alongside GitHub PRs and Jira issues!

---

## Features

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/todo` | Show help | `/todo` |
| `/todo add <text>` | Add a new todo | `/todo add Review PR #123` |
| `/todo list` | Show all todos | `/todo list` |
| `/todo done <id>` | Mark as complete | `/todo done 3` |
| `/todo delete <id>` | Remove a todo | `/todo delete 2` |
| `/todo edit <id> <text>` | Edit description | `/todo edit 1 Updated task` |

### Storage

- **Location**: `data/todos.json`
- **Format**: JSON per-user storage
- **Persistence**: Survives bot restarts
- **Privacy**: Each user has private todos
- **Auto-backup**: Gitignored (won't be committed)

### Integration with /mywork

Todos automatically appear in your `/mywork` command output:

```
📋 Your Pending Work

🐙 GitHub Pull Requests
[... your PRs ...]

📊 Jira Issues
[... your issues ...]

✅ Personal Todos
🔴 ⬜ 1. High priority task
🟡 ⬜ 2. Medium priority task
✅ ~3. Completed task~

Manage todos: /todo add, /todo done <id>, /todo list
```

---

## Advanced Usage

### Priority Levels

Todos can have priority levels (future enhancement):
- 🔴 High
- 🟡 Medium  
- 🟢 Low

Currently all todos default to medium priority.

### Completion Tracking

- Active todos show with ⬜
- Completed todos show with ✅ and strikethrough
- Recently completed (last 3) appear in `/mywork`
- All todos visible in `/todo list`

---

## Troubleshooting

### "/todo command not found"

1. Make sure you created the slash command in Slack
2. Reinstall the app after adding the command
3. Restart the bot: `./start_bot.sh`

### "No response from bot"

1. Check bot is running: Look for "⚡️ Bot is running"
2. Check Socket Mode is enabled
3. Check logs for errors

### "Todos not saving"

1. Check `data/` directory exists
2. Check write permissions
3. Check `data/todos.json` is created

---

## Demo Script

Perfect for Developer Week presentations:

```
Presenter: "Let me show you how I manage ALL my work in one place"

1. /mywork
   → Shows GitHub (15 PRs, 27 reviews) + Jira (16 issues)

2. "But I also have personal tasks that don't belong in GitHub or Jira"

3. /todo add Prepare slides for Developer Week demo
   → ✅ Added todo #1

4. /todo add Follow up with team on feedback
   → ✅ Added todo #2

5. /mywork
   → Now shows GitHub + Jira + 2 Personal Todos!

6. /todo done 1
   → ✅ Completed: ~Prepare slides for Developer Week demo~

7. /mywork
   → Shows 1 active todo + 1 recently completed

Presenter: "One command. Complete visibility. That's productivity!"
```

---

## Future Enhancements

See `FEATURES_AND_IMPROVEMENTS.md` for ideas:

- Priority setting: `/todo add --priority high Task name`
- Due dates: `/todo add --due tomorrow Task name`
- Categories/tags: `/todo add --tag urgent Task name`
- Reminders: Get notified about overdue todos
- Recurring todos: `/todo add --repeat daily Standup meeting`
- Team todos: Share todos with team members
- Todo templates: Quick task creation from templates

---

## Architecture

```
/todo command
    ↓
src/slack/bot.py (handle_todo_command)
    ↓
src/storage/todo_store.py (TodoStore class)
    ↓
data/todos.json (persistent storage)
    ↓
src/utils/formatter.py (format_todos)
    ↓
Slack Block Kit Response
```

---

**Questions?** Check the main [README.md](README.md) or open an issue!

