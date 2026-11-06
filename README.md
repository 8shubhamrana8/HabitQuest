
<div align="center">

# 🎯 HabitQuest
### *A gamified habit-tracking web application built to help you build better routines, earn XP, and level up your daily life.*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.x-green.svg?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-yellow.svg?style=flat&logo=javascript&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

</div>

---

**HabitQuest** is a feature-rich, full-stack web application designed to make habit-building engaging through gamification. By combining traditional streak tracking with RPG-style elements like user ranks, experience points (XP), and daily logs, it turns personal growth into an interactive journey.

---

## ✨ Core Features

* **🎮 Gamified Progression**: 
  * Earn Experience Points (XP) and level up your user rank as you complete daily habits.
  * Streak tracking to keep you motivated and accountable.
 
    <img width="100%" height="auto" alt="HabitTracker" src="https://github.com/user-attachments/assets/019db43c-3a0a-45bb-ae5b-afd7b22ee73d" />

* **📋 Dynamic Habit Management**:
  * Create, edit, and organize daily logs and custom habits seamlessly.
  * Interactive UI toggles powered by vanilla JavaScript for instant feedback.
 
  <img width="100%" height="auto" alt="ScreenRecording2026-11-06020725-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/cfc74f48-ac4c-4501-8412-8e427c2dcf10" />
  <img width="100%" height="auto" alt="ScreenRecording2026-11-06020800-ezgif com-video-to-gif-converter" src="https://github.com/user-attachments/assets/f2f6f293-d542-4e8c-8987-ed9969902291" />

* **📊 Analytics & History**:
  * Visual overview of past performance and completion logs.

* **🔒 Authentication & Security**:
  * Secure user registration, login, and session management using Django's built-in authentication system.
  
  <img width="100%" height="auto" alt="Screenshot 2026-11-06 020835" src="https://github.com/user-attachments/assets/3e4f8c0c-b681-47be-9bbb-3a77d678e55a" />
  <img width="100%" height="auto"  alt="Screenshot 2026-11-06 020900" src="https://github.com/user-attachments/assets/a1e52094-68ca-4176-b6e1-7f06775808d9" />

---

## 🛠️ Tech Stack

* **Backend**: Python, Django
* **Frontend**: HTML5, CSS3, JavaScript (ES6+)
* **Database**: SQLite (Development) / PostgreSQL-ready
* **Styling**: Bootstrap / Custom CSS
* **Version Control**: Git & GitHub

---

## 🚀 Getting Started

### Prerequisites
* Python 3.10 or higher installed on your machine.
* `pip` (Python package manager).

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone [https://github.com/8shubhamrana8/HabitQuest.git](https://github.com/8shubhamrana8/HabitQuest.git)
   cd HabitQuest

2. **Create and activate a virtual environment**

  Bash
  python -m venv venv
  # On Windows:
  venv\Scripts\activate
  # On macOS/Linux:
  source venv/bin/activate

3. **Install dependencies**
  pip install -r requirements.txt

4. **Apply database migrations**
  python manage.py makemigrations
  python manage.py migrate

5. **Create a superuser (optional, for Django Admin access)**
  python manage.py createsuperuser

6. **Run the development server**
  python manage.py runserver
  Open your browser and navigate to http://127.0.0.1:8000/.

### 📂 Project Structure

    HabitQuest/
    ├── habitquest_project/    # Django project settings and URLs
    ├── core/                  # Main Django app (models, views, forms, migrations)
    ├── static/                # Static assets (CSS, JavaScript, images)
    ├── templates/             # HTML templates with Django template inheritance
    ├── manage.py              # Django command-line utility
    └── requirements.txt       # Project dependencies
