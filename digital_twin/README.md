# Plant Doctor 🌱

Plant Doctor is an AI-powered web application that helps users diagnose plant diseases, providing immediate treatment plans, long-term care advice, and product recommendations.

## Features

*   **AI Diagnosis:** Upload or snap a photo of a plant to identify diseases using Gemini AI.
*   **Actionable Advice:** Get immediate action plans and long-term care guides.
*   **Product Recommendations:** Receive curated product suggestions (e.g., fertilizers, pesticides) with shopping links.
*   **Dashboard:** specialized dashboard to track your scanning history and saved diagnoses.
*   **Blog:** Access a curated list of plant care articles powered by Wikipedia data.
*   **User Profiles:** Manage your profile and view your garden's health.

## Prerequisites

*   Python 3.10+
*   A Google Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/plantdoctor.git
    cd plantdoctor
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```
    Add the following content to `.env`:
    ```env
    DEBUG=True
    SECRET_KEY=your-secure-secret-key-here
    GEMINI_API_KEY=your_google_gemini_api_key_here
    ```

5.  **Run Database Migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Start the Development Server:**
    ```bash
    python manage.py runserver
    ```

7.  **Access the App:**
    Open your browser and navigate to `http://127.0.0.1:8000`.

## Tech Stack

*   **Backend:** Django 6.0.1
*   **Frontend:** HTML, Tailwind CSS
*   **AI Model:** Google Gemini 1.5 Flash (`gemini-flash-latest`)
*   **Database:** SQLite (Default)

## License

MIT License.
