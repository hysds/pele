import os, sys, click, unittest, coverage
from flask_migrate import Migrate, MigrateCommand

from pele import create_app, db

COV = coverage.coverage(
    branch=True,
    include='pele/*',
    omit=[
        'pele/static/*',
        'pele/templates/*'
    ]
)
COV.start()

env = os.environ.get('FLASK_ENV', 'production')
app = create_app('pele.settings.%sConfig' % env.capitalize())
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User)


@app.cli.command()
def test():
    """Runs the unit tests without test coverage."""

    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    print(tests)
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@app.cli.command()
def cov():
    """Runs the unit tests with coverage."""

    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@app.cli.command()
def create_db():
    """Creates the db tables."""

    dbdir = app.config['DB_DIR']
    if not os.path.isdir(dbdir):
        os.makedirs(dbdir, 0o755)
    db.create_all()


@app.cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()
