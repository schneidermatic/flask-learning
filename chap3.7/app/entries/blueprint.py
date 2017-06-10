from flask import Blueprint
from flask import render_template
from flask import request
from helpers import object_list
from models import Entry, Tag
from app import app
entries = Blueprint('entries', __name__, template_folder='templates')

def entry_list(template, query, **context):
    app.logger.info("---> Hello")
    search = request.args.get('q')
    if search:
        query = query.filter(
            (Entry.body.contains(search)) |
            (Entry.title.contains(search)))
    return object_list(template, query, **context)

@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    #return object_list('entries/index.html', entries)
    return entry_list('entries/index.html', entries)

@entries.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    return object_list('entries/tag_index.html', tags)

@entries.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return object_list('entries/tag_detail.html', entries, tag=tag)

@entries.route('/<slug>/')
def detail(slug):
    entry = Entry.query.filter(Entry.slug == slug).first_or_404() 
    return render_template('entries/detail.html', entry=entry)

