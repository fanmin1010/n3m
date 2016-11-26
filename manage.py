from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from application.app import app, db, socketio

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()

@manager.command
def start_app():
    """run the app."""
    socketio.run(app,
                host='0.0.0.0',
                port=5000,
                use_reloader=False,
                debug=True)

if __name__ == '__main__':
    manager.run()
