# Pollz Backend (Django)

## Prerequisites
- Docker
- Docker Compose

## Setup

1. **Clone and navigate to backend**
```bash
cd back/
```

2. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Run with Docker Compose**
```bash
docker-compose up --build
```

Server will be available at `http://localhost:6969`
Admin panel will be available at `http://localhost:6969/admin`

## Available Commands
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Add sample data (creates departments, huels, election candidates, clubs - NO votes)
docker-compose exec web python manage.py populate_sample_data

# Add huel
docker-compose exec web python manage.py populate_huel_courses

#Add Departments
docker-compose exec web python manage.py populate_oasis_data.py

# Add election candidates
docker-compose exec web python manage.py add_election_candidates

# Stop services
docker-compose down
```