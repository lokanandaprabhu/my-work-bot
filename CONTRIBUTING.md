# 🤝 Contributing to My Work Bot

Thank you for your interest in contributing to My Work Bot! This guide will help you get started.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/my-work-bot.git
   cd my-work-bot
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   ```bash
   cp env.example .env
   # Edit .env with your credentials
   ```

5. **Run the Bot**
   ```bash
   python run.py
   ```

## Project Structure

```
my-work-bot/
├── src/
│   ├── slack/          # Slack bot implementation
│   ├── github/         # GitHub API client
│   ├── jira/           # Jira API client
│   └── utils/          # Utilities and formatters
├── tests/              # (Future) Unit tests
└── docs/               # (Future) Additional documentation
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where applicable
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

## Adding New Features

### Adding a New Integration (e.g., GitLab)

1. Create a new module: `src/gitlab/client.py`
2. Implement the client class with required methods
3. Add formatter support in `src/utils/formatter.py`
4. Update bot to fetch and display data
5. Add environment variables to `env.example`
6. Update README with setup instructions

### Adding New Slash Commands

1. Add handler in `src/slack/bot.py`:
   ```python
   @self.app.command("/newcommand")
   def handle_new_command(ack, respond, command):
       ack()
       # Implementation
   ```

2. Update Slack app settings with new command
3. Document in README

### Improving Message Formatting

Edit `src/utils/formatter.py` to modify Slack Block Kit output.

## Testing

(Future implementation)

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src
```

## Submitting Changes

1. Create a feature branch
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. Make your changes with clear commit messages
   ```bash
   git commit -m "Add GitLab integration support"
   ```

3. Push to your fork
   ```bash
   git push origin feature/my-new-feature
   ```

4. Open a Pull Request with:
   - Clear description of changes
   - Any relevant screenshots
   - Testing steps

## Feature Ideas

See the "Suggestions for Improvement" section in README.md for ideas!

## Questions?

Open an issue or reach out to the maintainers.

Happy coding! 🚀

