# Contributing to Silent Signal

Thank you for your interest in contributing to Silent Signal!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

```bash
# Install dependencies
pip install -r requirements.txt
cd frontend && npm install

# Start development environment
docker-compose up -d
python scripts/init_db.py

# Run application
uvicorn backend.main:app --reload
```

## Code Style

- Python: Follow PEP 8
- JavaScript: Use ES6+ features
- Use meaningful variable names
- Add comments for complex logic

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=backend
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Reporting Issues

- Use GitHub Issues
- Provide clear description
- Include steps to reproduce
- Add relevant logs/screenshots

## Questions?

Open a discussion on GitHub or reach out to maintainers.
