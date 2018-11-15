from flask import render_template

from . import main
from .. import login_manager
from ..models import User, Bookmark, Tag


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', new_bookmarks=Bookmark.newest(5))


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


# this makes this globaly available to all templates.
# don't add () as this would call the func (thus query db) prior to any template rendering.
# if this is needed in a template call the function in the template instead of here.
@main.app_context_processor
def inject_tags():
    return dict(all_tags=Tag.all)
