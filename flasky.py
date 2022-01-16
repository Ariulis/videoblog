import os
import click

from flask_migrate import Migrate
from dotenv import load_dotenv

from app import db, create_app
from app.models import User, Video

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app(os.getenv('FLASK_ENV'))
migrate = Migrate(app, db)
client = app.test_client()


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, client=client, Video=Video, User=User)


@app.cli.command('test')
def test():
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
