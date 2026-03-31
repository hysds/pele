"""CLI commands for pele."""
import os
from pele import create_app, db


def init_db():
    """Initialize the pele database."""
    env = os.environ.get('FLASK_ENV', 'production')
    app = create_app(f'pele.settings.{env.capitalize()}Config')
    
    with app.app_context():
        dbdir = app.config['DB_DIR']
        os.makedirs(dbdir, 0o755, exist_ok=True)
        db.create_all()
        print(f"Database initialized at {dbdir}")


if __name__ == '__main__':
    init_db()
