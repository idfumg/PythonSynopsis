# export FLASK_DEBUG=1 FLASK_APP=microblog.py && flask run

from app import app, db
from app.models import User, Post

# export FLASK_APP=microblog.py && flask shell
@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Post': Post,
    }
