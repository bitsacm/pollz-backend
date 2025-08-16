# Contributing to Pollz Backend

## Setup
1. Fork the repository
2. Clone your fork: `git clone <your-fork-url>`
3. Create `.env` from `.env.example`
4. Run: `docker-compose up --build`

## Development Workflow
1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes
3. Test locally: `docker-compose exec web python manage.py test`
4. Run migrations if needed: `docker-compose exec web python manage.py migrate`
5. Commit with clear message
6. Push and create PR (see PR Guidelines below)

## Code Standards
- Follow PEP 8 style guide
- Add docstrings to functions/classes
- Write tests for new features
- Use meaningful variable names
- Keep functions focused and small

## Before Submitting PR
- [ ] Tests pass
- [ ] No hardcoded credentials
- [ ] Database migrations included
- [ ] Requirements.txt updated if needed
- [ ] Code follows Django best practices

## GitHub PR Guidelines

### PR Title Format
Use conventional commit format: `type(scope): description`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
- `feat(auth): add Google OAuth login`
- `fix(voting): resolve duplicate vote issue`
- `docs(api): update endpoint documentation`
- `refactor(models): optimize database queries`

### PR Description
- Clearly describe what changes were made
- Include screenshots for UI changes
- Reference related issues using `Fixes #123`
- List any breaking changes
- Mention if migrations are included

### Branch Naming
- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/documentation-update` - Documentation
- `refactor/component-name` - Refactoring

## Project Structure
- `main/` - Core voting functionality
- `superchat/` - Chat/messaging features
- `pollz/` - Django settings and configuration
- `manage.py` - Django management commands