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

### Razorpay Setup (Required for SuperChat payments)

1. **Get Razorpay API Keys:**
   - Visit [Razorpay Dashboard](https://dashboard.razorpay.com/)
   - Sign up/Login to your account
   - Go to **Account & Settings** → **API Keys**
   - Generate **Test Mode** keys for development
   - Copy the **Key ID** and **Key Secret**

2. **Configure Razorpay in .env:**
```bash
RAZORPAY_KEY_ID=rzp_test_your_key_id_here
RAZORPAY_KEY_SECRET=your_key_secret_here
RAZORPAY_WEBHOOK_SECRET=your_custom_webhook_secret
```

3. **Setup Webhook for Local Development (using ngrok):**
   
   **Install ngrok:**
   ```bash
   # On macOS
   brew install ngrok
   
   # On Ubuntu/Debian
   sudo apt install ngrok
   
   # Or download from https://ngrok.com/download
   ```
   
   **Expose your local server:**
   ```bash
   # In a separate terminal, expose port 8000 (or your Django port)
   ngrok http 8000
   ```
   
   **Configure Razorpay Webhook:**
   - Copy the ngrok HTTPS URL (e.g., `https://abc123.ngrok-free.app`)
   - Go to [Razorpay Dashboard](https://dashboard.razorpay.com/) → **Webhooks**
   - Click **Create Webhook**
   - **URL:** `https://your-ngrok-url.ngrok-free.app/api/superchat/razorpay-webhook/`
   - **Events:** Select `payment.captured`
   - **Secret:** Use the same value as `RAZORPAY_WEBHOOK_SECRET` in your .env
   - Click **Create**

   **Update Django ALLOWED_HOSTS:**
   ```bash
   # Add your ngrok domain to settings.py ALLOWED_HOSTS
   ALLOWED_HOSTS = [
       'localhost',
       '127.0.0.1',
       'your-ngrok-domain.ngrok-free.app',  # Add this
   ]
   ```

4. **Test the Integration:**
   - Start your Django server with Docker Compose
   - Keep ngrok running in a separate terminal
   - Test SuperChat payments through the frontend
   - Check Razorpay Dashboard for payment status
   - Verify webhook calls in ngrok terminal logs

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