# Quiz Master V2

A full-stack quiz management system built with Flask (backend), Vue 3 + Vite (frontend), Celery (task queue), and Redis (cache & broker).

## Features

- User registration and login
- Admin dashboard for managing subjects, chapters, quizzes, and questions
- Quiz attempt and scoring
- Real-time updates with Celery and Redis

## Prerequisites

- Python 3.8+
- Node.js & npm
- Redis server (will be started automatically)
- Celery (will be started automatically)
- All Python and Node dependencies installed (`pip install -r requirements.txt` and `npm install` in `frontend`)

- Create a `.env` file in the `backend` directory with the following environment variables:
  ```
  GEMINI_API_KEY=your_gemini_api_key_here
  EMAIL_PASSWORD=your_email_password_here
  EMAIL_ID=your_email_id_here
  ```

## Quick Start

1. **Install dependencies:**
   - Python:  
     ```bash
     pip install -r requirements.txt
     ```
   - Node.js:  
     ```bash
     cd frontend
     npm install
     cd ..
     ```

2. **Run the project:**
   ```bash
   python3 run.py
   ```

   This will:
   - Start Redis server
   - Start Celery worker and beat
   - Start the Vue frontend dev server
   - Start the Flask backend

3. **Access the app:**
   - Frontend: [http://localhost:5173](http://localhost:5173)
   - Backend API: [http://localhost:8001](http://localhost:8001)

## Default Admin Login

- **Email:** `admin@quiz.com`
- **Password:** `admin123`

---

**Note:**  
If you do not have Redis or Celery installed, please install them