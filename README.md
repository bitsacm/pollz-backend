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

## Troubleshooting

### Database Collation Version Mismatch Warning

When starting the services with `docker-compose up`, you may see a warning in the logs like this:
`WARNING: database "template1" has a collation version mismatch`

This happens if the Docker image for PostgreSQL has been updated with a newer version of its operating system libraries since the database was first created.

**To fix this**, you need to connect to the running database container and refresh the collation version.

1.  Start the database service in the background:
    ```bash command
    docker-compose up -d db
    ```

2.  Find your database username in the `.env` file (the value of `POSTGRES_USER=`).

3.  Connect to the PostgreSQL prompt inside the container, replacing `your_username` with the actual username:
    ```bash
    docker-compose exec db psql -U your_username -d pollz_db
    ```

4.  Run the following SQL commands one by one:
    ```sql
    REINDEX DATABASE pollz_db;

    ALTER DATABASE pollz_db REFRESH COLLATION VERSION;

    UPDATE pg_database SET datallowconn = true WHERE datname = 'template0';
    \c template0 '(\c = to connect)'

    ALTER DATABASE template0 REFRESH COLLATION VERSION;
    \c template1

    ALTER DATABASE template1 REFRESH COLLATION VERSION;

    UPDATE pg_database SET datallowconn = false WHERE datname = 'template0';

    \q '(to quit)'
    ```

5.  You can now restart all services. The warning should be gone.
    ```bash
    docker-compose down
    docker-compose up

    'Now, carefully watch the startup logs in your terminal. WARNING: database ... has a collation version mismatch message should no longer appear. If its gone, you have successfully fixed the issue!'
    ```