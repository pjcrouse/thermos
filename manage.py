from thermos import app, db
from thermos.models import User, Bookmark, Tag # even though Bookmark isn't used directly it's needed by flask_migrate
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def init_db():
    db.create_all()
    db.session.add(User(username='pcrouse', email='patcrouse@gmail.com', password='test'))
    db.session.add(User(username='xcrouse', email='xandercrouse@gmail.com', password='test'))
    db.session.commit()
    print("Initialized the database")

@manager.command
def insert_data():
    pcrouse = User(Userusername='pcrouse', email='patcrouse@gmail.com', password='test')
    db.session.add(pcrouse)

    def add_bookmark(url, description, tags):
        db.session.add(Bookmark(url=url, description=description, user=reindert,
                                tags=tags))

    for name in ["python", "flask", "webdev", "programming", "training", "news", "orm", "databases", "emacs", "gtd", "django"]:
        db.session.add(Tag(name=name))
    db.session.commit()

    add_bookmark("http://www.pluralsight.com", "Pluralsight. Hardcore developer training.", "training,programming,python,flask,webdev")
    add_bookmark("http://www.python.org", "Python - my favorite language", "python")
    add_bookmark("http://flask.pocoo.org", "Flask: Web development one drop at a time.", "python,flask,webdev")
    add_bookmark("http://www.reddit.com", "Reddit. Frontpage of the internet", "news,coolstuff,fun")
    add_bookmark("http://www.sqlalchemyorg", "Nice ORM framework", "python,orm,databases")


    xcrouse = User(username="xcrouse", email="xandercrouse@gmail.com", password="test")
    db.session.add(xcrouse)
    db.session.commit()
    print('Initialized the database')

@manager.command
def drop_db():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()
        print("Dropped the database")


if __name__ == "__main__":
    manager.run()
