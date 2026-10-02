# NXTWALK

NXTWALK is a Django-based website development and digital marketing platform.

## Tech Stack
- Python 3.12+
- Django 5.2+
- PostgreSQL
- HTML5 / CSS3 / JavaScript
- Django Templates

## Quick Start

### 1. Create virtual environment
```bash
python -m venv venv
```

Windows:
```powershell
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
Copy `.env.example` to `.env` and update PostgreSQL credentials.

### 4. Create database
Create a PostgreSQL database named `nxtwalk`.

### 5. Run migrations
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Start development server
```bash
python manage.py runserver
```

Open: http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/
