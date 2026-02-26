# Free Hosting Options for Plant Doctor

Yes, you can host this project for free! Since this project uses **Django** (Python), **SQLite** (Database), and **Media Files** (User uploaded images), your best options are:

## Option 1: PythonAnywhere (Recommended for Beginners) 🏆

**Why:** It supports SQLite and local file storage (like uploaded images) out of the box. It is the easiest way to deploy this specific project without changing code.

*   **Pros:**
    *   Persistent filesystem (Your database and images won't disappear).
    *   Easy "One-click" style setup for Django.
    *   Free subdomain (e.g., `yourname.pythonanywhere.com`).
*   **Cons:**
    *   **Restricted Internet:** Free accounts can only connect to specific "whitelisted" websites.
    *   *Note:* You may need to email PythonAnywhere support to ask if `generativelanguage.googleapis.com` (Gemini API) allows connections on the free tier. They are usually helpful with this.

**Quick Setup Guide:**
1.  Sign up at [pythonanywhere.com](https://www.pythonanywhere.com/).
2.  Go to the **Web** tab and "Add a new web app".
3.  Choose **Django** -> **Python 3.10**.
4.  In the **Bash Console**, clone your repo:
    ```bash
    git clone https://github.com/yourusername/Plantdoctor.git
    ```
5.  Install dependencies:
    ```bash
    pip install -r Plantdoctor/requirements.txt
    ```
6.  Edit the **WSGI configuration file** (link in Web tab) to point to your project.
7.  Add your environment variables (API Keys) in the WSGI file or `.env`.

## Option 2: Render (Modern / Scalable) 🚀

**Why:** It is a modern cloud platform that works like professional production environments.

*   **Pros:**
    *   Great integration with GitHub (Auto-deploys when you push code).
    *   No whitelist restrictions (Gemini API will definitely work).
*   **Cons:**
    *   **Ephemeral Filesystem:** The free tier **deletes** all local files when the server restarts (which happens often).
    *   **Impact:** Your SQLite database will reset, and user-uploaded images will vanish.
    *   **Fix:** To use Render, you *must* change your project to use **PostgreSQL** (external DB) and **Cloudinary/AWS S3** (for images). This requires code changes.

## Option 3: Ngrok (Temporary / Demo) ⏱️

**Why:** If you just want to show the project to a friend *right now* without setting up a server.

1.  Run your server locally: `python manage.py runserver`
2.  Download and run [Ngrok](https://ngrok.com/): `ngrok http 8000`
3.  It gives you a public URL (e.g., `https://random-name.ngrok.io`) that forwards to your computer.
4.  *Note:* Stops working when you turn off your computer.

## Summary

For **Plant Doctor**, start with **PythonAnywhere**. It handles your database and image uploads without needing any code changes.
