import os
import shutil
from pathlib import Path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# On Vercel, copy the pre-built SQLite DB from the repo into /tmp (writable)
# so data (seeds, migrations) is available on cold starts.
if os.getenv("VERCEL"):
    src = Path(__file__).resolve().parent.parent / "db.sqlite3"
    dst = Path("/tmp/db.sqlite3")
    if src.exists() and not dst.exists():
        shutil.copy2(src, dst)

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
