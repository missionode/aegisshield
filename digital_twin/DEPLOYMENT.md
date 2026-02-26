# Deployment Guide: Plant Doctor

Follow these steps to deploy the Plant Doctor application on a new server (e.g., VPS, Cloud Instance, or another local machine).

## Prerequisites

*   **Python 3.10 or higher** installed on the server.
*   **Git** installed.
*   **Google Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/).

## 1. Clone the Repository

Clone the project to your desired directory:

```bash
git clone https://github.com/yourusername/plantdoctor.git
cd plantdoctor
```

## 2. Set Up Virtual Environment

Create and activate a virtual environment to isolate dependencies:

```bash
python3 -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

## 3. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

## 4. Environment Configuration

Create a `.env` file in the project root to store sensitive configuration. You can copy the structure from a `.env.example` if available, or use the template below:

```bash
touch .env
```

**Add the following content to `.env`:**

```env
# Set to False in production
DEBUG=False

# Generate a strong, random secret key for production
SECRET_KEY=your-secure-production-secret-key-here

# Your Google Gemini API Key
GEMINI_API_KEY=your_google_gemini_api_key_here

# Comma-separated list of allowed hostnames/IPs
# Example: .yourdomain.com, 203.0.113.1
ALLOWED_HOSTS=localhost,127.0.0.1,[::1],your-server-ip-or-domain
```

## 5. Database Setup

Apply the database migrations to set up the SQLite database (or configure a different database in `settings.py` if needed):

```bash
python manage.py migrate
```

## 6. Static Files (Production Only)

If `DEBUG=False`, Django won't serve static files automatically. You need to collect them into a single directory:

```bash
python manage.py collectstatic
```

*Note: You will need a web server like Nginx or Apache, or use WhiteNoise to serve these files in production.*

## 7. Create Superuser (Admin)

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

## 8. Run the Server

### For Development/Testing:
```bash
python manage.py runserver 0.0.0.0:8000
```
Access the site at `http://your-server-ip:8000`.

### For Production:
Use a production-grade WSGI server like **Gunicorn**:

1.  Install Gunicorn:
    ```bash
    pip install gunicorn
    ```
2.  Run the application:
    ```bash
    gunicorn plant_doctor.wsgi:application --bind 0.0.0.0:8000
    ```

## 9. Troubleshooting

*   **API Quota Errors:** Ensure your Gemini API key is valid and has quota available.
*   **Static Files Missing:** If images/CSS are missing in production, ensure you ran `collectstatic` and configured your web server correctly.
*   **Database Issues:** If using a database other than SQLite, check your `DATABASES` setting in `plant_doctor/settings.py`.
