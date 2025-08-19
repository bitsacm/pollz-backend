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
