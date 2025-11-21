#!/bin/bash
# Start My Work Bot

cd "$(dirname "$0")"

echo "════════════════════════════════════════════════════════════"
echo "🤖 STARTING MY WORK BOT"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "✅ GitHub integration: ENABLED"
echo "✅ Slack integration: ENABLED (Red Hat Sandbox)"
echo "⏸️  Jira integration: DISABLED"
echo ""
echo "📱 Test the bot:"
echo "   1. Open Red Hat Slack Sandbox"
echo "   2. Type: /mywork"
echo "   3. See your 15 PRs and 27 review requests!"
echo ""
echo "🛑 To stop the bot: Press Ctrl+C"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""

./venv/bin/python run.py
