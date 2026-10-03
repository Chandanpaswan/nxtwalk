# NXTWALK

NXTWALK is a modular Django website for a web development and digital marketing company. It includes public marketing pages, database-managed services and editorial content, project stories, contact intake, authentication, and technical SEO foundations.

## Features

- Responsive agency website with home, about, services, portfolio, case studies, journal, legal, and contact pages.
- Database-managed services, projects and galleries, case studies, testimonials, categories, tags, blog posts, site settings, contact messages, and user profiles.
- Django Admin search, filters, slug helpers, pagination, bulk contact follow-up, and project gallery management.
- Contact form with validation, service/budget fields, and a honeypot spam check.
- Admin-managed company/contact settings, ordered social links, navigation and footer columns, editable pages, and newsletter subscribers with CSV export.
- Separate project enquiries with a lead-status pipeline and an Admin dashboard with live database counts.
- Official Instagram, Facebook, X, LinkedIn, YouTube and WhatsApp links are seeded into editable records. The contact email intentionally remains blank until the owner supplies the real address.
- Django authentication, registration, profile editing, password change, and password reset.
- Dynamic page metadata, canonical URLs, Open Graph/Twitter tags, Organization/Service/Article schema, XML and HTML sitemaps, and robots.txt.
- SQLite database configuration, environment-based production security, and WhiteNoise static file handling.

## Technology

Python 3.12+, Django 5.2, SQLite, Django Templates, HTML, CSS, vanilla JavaScript, Pillow, WhiteNoise, and Gunicorn.

## Local Setup

### 1. Create and activate a virtual environment

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```

Use an installed Python 3.12+ version if `py -3.12` is unavailable.

### 2. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configure SQLite

Copy the environment example. SQLite creates the configured database file automatically when migrations run; no database server or credentials are needed.

```powershell
Copy-Item .env.example .env
```

Set `SQLITE_PATH` if the database file should live somewhere other than the project root. Generate a local secret with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Never commit `.env` or real credentials. The repository ignores `.env`, virtual environments, media uploads, and generated static output.

### 4. Apply migrations and create an administrator

```powershell
python manage.py migrate
python manage.py createsuperuser
```

The service catalogue is populated by a reversible data migration. Portfolio items, case studies, testimonials, and blog posts should be created in Admin only when approved content is available.

The initial site-management migrations add the official social profiles, WhatsApp number, editable menu/footer links, and FAQ page. Review or change them under the `Website` section in Admin. Add the real contact email and any business address/hours only after those details are confirmed.

### 5. Run the site

This is a Django application, not a static HTML site. Do not open the workspace with VS Code Live Server (commonly port `5500`); it serves the folder and cannot execute Django templates. Start the server below and open `http://127.0.0.1:8000/` instead.

```powershell
python manage.py runserver
```

- Website: http://127.0.0.1:8000/
- Django Admin: http://127.0.0.1:8000/admin/
- Staff dashboard: http://127.0.0.1:8000/admin-dashboard/
- XML sitemap: http://127.0.0.1:8000/sitemap.xml
- HTML sitemap: http://127.0.0.1:8000/sitemap/
- Robots: http://127.0.0.1:8000/robots.txt

## Environment Variables

See `.env.example` for the complete list. Core variables are `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, SQLite `SQLITE_PATH` and `SQLITE_TIMEOUT`, `SECURE_SSL_REDIRECT`, `SECURE_COOKIES`, `SECURE_HSTS_*`, and SMTP `EMAIL_*` values. Set `DEFAULT_FROM_EMAIL` to an address NXTWALK owns once that address is confirmed. Local development uses the console email backend by default; production should use an authenticated SMTP provider and private environment secrets.

## Common Commands

```powershell
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py test
python manage.py collectstatic --noinput
```

Run migrations only after reviewing generated migration files. The SQLite file is ignored by Git; back it up and place it on persistent storage in production. SQLite is suitable for a single application instance and modest write concurrency; coordinate database access before running multiple application workers across hosts.

## Production Deployment

1. Install dependencies in the deployment environment and provision persistent storage for the SQLite database file.
2. Set a unique `SECRET_KEY`, `DEBUG=False`, a restrictive `ALLOWED_HOSTS`, and a persistent `SQLITE_PATH` through the platform's environment configuration.
3. Set `CSRF_TRUSTED_ORIGINS` to HTTPS origins. Enable `SECURE_SSL_REDIRECT` and `SECURE_COOKIES` behind HTTPS; configure HSTS only after HTTPS is verified end to end. Enable `TRUST_X_FORWARDED_PROTO` only when the application is behind a trusted proxy that sets `X-Forwarded-Proto`.
4. Configure SMTP credentials through environment variables. Do not use the development console email backend in production.
5. Run `python manage.py migrate` and `python manage.py collectstatic --noinput` as release steps. Ensure the SQLite file's directory is writable and retained across deploys.
6. Start Gunicorn with `gunicorn config.wsgi:application`. Configure the platform's HTTPS proxy headers only when its trusted proxy setup is known.
7. Provision persistent media storage or a private object-storage service for user-uploaded images; WhiteNoise serves static assets, not uploaded media.

Before deployment, verify `python manage.py check --deploy` against the actual HTTPS, proxy, host, database, and secret configuration.

## SEO and Content

SEO fields are shared by services, posts, projects, and case studies. Blank titles and descriptions fall back to the page title and summary. Published content enters the XML sitemap; draft and unpublished items are excluded. Add approved images with descriptive alt text in Admin. The NXTWALK Organization schema deliberately avoids inventing a street address or local-business details.

## Structure

```text
config/                 Django settings and root routes
apps/accounts/          Authentication and user profiles
apps/blog/              Posts, categories, tags, search, pagination
apps/case_studies/      Case study narratives
apps/contact/           Contact form and submissions
apps/portfolio/         Projects and image galleries
apps/seo/               Shared SEO fields and XML sitemap classes
apps/services/          Service catalogue
apps/testimonials/      Client testimonials
apps/website/           Home, legal, sitemap, dashboard, site settings
templates/              Shared shell and app templates
static/css/             Brand and responsive stylesheet
static/js/              Modular navigation, animation, cursor, and scroll effects
media/                  Runtime image uploads (not committed)
```
