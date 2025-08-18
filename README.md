# Pollz Backend (Django)

## Overview
Pollz Backend is the core service powering **Pollz**, built with Django.  
It provides APIs for voting, chat, and other student community features.

---

## Prerequisites
- Linux or macOS (preferred). On Windows, use **WSL** or dual boot.
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

> ⚠️ Note: Your system may support either `docker-compose` or `docker compose`.  
> Use the same consistently. Prepend `sudo` if you encounter permission errors.

---

## Setup Instructions

### Option 1: Clone All Repositories (recommended for full-stack setup)

1. **Fork** the repositories on GitHub (backend, frontend, websocket) from the original organization:  

   * Backend: [bitsacm/pollz-backend](https://github.com/bitsacm/pollz-backend)  
   * Frontend: [bitsacm/pollz-frontend](https://github.com/bitsacm/pollz-frontend)  
   * Websocket: [bitsacm/pollz-websocket](https://github.com/bitsacm/pollz-websocket)  

2. **Clone your forks** into a single `pollz` folder (replace `<your-github-username>` with yours):

   ```bash
   # Create a parent folder to keep all Pollz repos together
   mkdir pollz
   cd pollz

   # Clone backend
   git clone https://github.com/<your-github-username>/pollz-backend.git

   # Clone frontend
   git clone https://github.com/<your-github-username>/pollz-frontend.git

   # Clone websocket
   git clone https://github.com/<your-github-username>/pollz-websocket.git

3. **Add upstream remotes** to fetch updates from the official repos:

   ```bash
   cd pollz-backend
   git remote add upstream https://github.com/bitsacm/pollz-backend.git
   cd ..

   cd pollz-frontend
   git remote add upstream https://github.com/bitsacm/pollz-frontend.git
   cd ..

   cd pollz-websocket
   git remote add upstream https://github.com/bitsacm/pollz-websocket.git
   cd ..
   ```

---

### Option 2: Clone Backend Only

1. **Fork** the repository on GitHub.

2. **Clone your fork** (replace `<your-github-username>`):

   ```bash
   git clone https://github.com/<your-github-username>/pollz-backend.git
   cd pollz-backend
   ```

3. *(Optional but recommended for contributors)* Add the original repo as upstream:

   ```bash
   git remote add upstream https://github.com/bitsacm/pollz-backend.git
   git fetch upstream
   ```

---

### Setup Environment

```bash
cp .env.example .env
# Edit .env with your credentials
```

---

### Run with Docker Compose

```bash
docker-compose up --build
```

* Server: [http://localhost:6969](http://localhost:6969)
* Admin Panel: [http://localhost:6969/api/hitler/](http://localhost:6969/api/hitler)

---

## Available Commands

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser (access admin panel with these credentials)
docker-compose exec web python manage.py createsuperuser

# Add sample data (departments, hostels, election candidates, clubs - NO votes)
docker-compose exec web python manage.py populate_sample_data

# Add hostel courses
docker-compose exec web python manage.py populate_huel_courses

# Add departments
docker-compose exec web python manage.py populate_oasis_data

# Add election candidates
docker-compose exec web python manage.py add_election_candidates

# Stop services
docker-compose down
```

---

## Project Structure

* `main/` - Core voting functionality
* `superchat/` - Chat/messaging features
* `pollz/` - Django settings and configuration
* `manage.py` - Django management commands

---

## Contributing

We ❤️ contributions!

If you’d like to contribute, please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

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
