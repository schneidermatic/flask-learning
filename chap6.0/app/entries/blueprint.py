import os
from flask import Blueprint
from flask import flash
from flask import render_template
from flask import request
from helpers import object_list
from models import Entry, Tag
from app import app
from app import db
from entries.forms import EntryForm
from entries.forms import ImageForm
from flask import redirect
from flask import url_for
from sqlalchemy.orm import sessionmaker
from werkzeug import secure_filename
from flask.ext.login import login_required
from flask import g

entries = Blueprint('entries', __name__, template_folder='templates')

#def filter_status_by_user(query):
#    if not g.user.is_authenticated:
#        return query.filter(Entry.status == Entry.STATUS_PUBLIC)
#    else:
#        return query.filter(Entry.status.in_((Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)))

def filter_status_by_user(query):
    if not g.user.is_authenticated:
        return query.filter(Entry.status == Entry.STATUS_PUBLIC)
    else:
        query = query.filter(
          (Entry.status == Entry.STATUS_PUBLIC) |
          (( Entry.author == g.user ) &
           ( Entry.status != Entry.STATUS_DELETED)))
        return query

def entry_list(template, query, **context):
    app.logger.info("---> Hello")

    query = filter_status_by_user(query)

    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
    query = query.filter(Entry.status.in_(valid_statuses))

    if request.args.get('q'):
        search = request.args['q']
        query = query.filter(Entry.body.contains(search) |
                            (Entry.title.contains(search)))

    return object_list(template, query, **context)

#def get_entry_or_404(slug):
#    valid_statuses = (Entry.STATUS_PUBLIC, Entry.STATUS_DRAFT)
#    entry = Entry.query.filter((Entry.slug == slug) & (Entry.status.in_(valid_statuses))).first_or_404()
#    return entry

def get_entry_or_404(slug, author=None):
    query = Entry.query.filter(Entry.slug == slug)
    if author:
        query = query.filter(Entry.author == author)
    else:
        query = filter_status_by_user(query)
    return query.first_or_404()

@entries.route('/')
def index():
    entries = Entry.query.order_by(Entry.created_timestamp.desc())
    #return object_list('entries/index.html', entries)
    return entry_list('entries/index.html', entries)

@entries.route('/tags/')
def tag_index():
    tags = Tag.query.order_by(Tag.name)
    return object_list('entries/tag_index.html', tags)

@entries.route('/image-upload/', methods=['GET','POST'])
@login_required
def image_upload():
    if request.method == 'POST':
        form = ImageForm(request.form)
        if form.validate():
            image_file = request.files['file']
            filename = os.path.join(app.config['IMAGES_DIR'], secure_filename(image_file.filename))
            image_file.save(filename)
            flash('Saved %s' % os.path.basename(filename),'success')
            return redirect(url_for('entries.index'))
    else:
        form = ImageForm()

    return render_template('entries/image_upload.html', form=form)

@entries.route('/tags/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    entries = tag.entries.order_by(Entry.created_timestamp.desc())
    return object_list('entries/tag_detail.html', entries, tag=tag)

@entries.route('/<slug>/')
def detail(slug):
    #entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    entry = get_entry_or_404(slug)
    return render_template('entries/detail.html', entry=entry)

@entries.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        form = EntryForm(request.form)
        if form.validate():
            entry = form.save_entry(Entry(author=g.user))
            for tag in entry.tags:
                app.logger.info("***> " + str(tag.id) + "|" + str(tag.name))
            db.session.add(entry)
            db.session.commit()
            flash('Entry "%s" created successfully.' % entry.title, 'success')
            return redirect(url_for('entries.detail', slug=entry.slug))
    else:
        form = EntryForm()

    return render_template('entries/create.html', form=form)

@entries.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit(slug):
    #entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    entry = get_entry_or_404(slug)
    if request.method == 'POST':
        app.logger.info("===> edit")
        form = EntryForm(request.form, obj=entry)
        if form.validate():
            entry = form.save_entry(entry)
            for tag in entry.tags:
                app.logger.info("***> " + str(tag.id) + "|" + str(tag.name))
            db.session.add(entry)
            db.session.commit()
            flash('Entry "%s" has been saved.' % entry.title, 'success')
            return redirect(url_for('entries.detail',slug=entry.slug))
    else:
        form = EntryForm(obj=entry)

    return render_template('entries/edit.html', entry=entry, form=form)


@entries.route('/<slug>/delete/', methods=['GET', 'POST'])
@login_required
def delete(slug):
    #entry = Entry.query.filter(Entry.slug == slug).first_or_404()
    entry = get_entry_or_404(slug)
    if request.method == 'POST':
        entry.status = Entry.STATUS_DELETED
        db.session.add(entry)
        db.session.commit()
        flash('Entry "%s" has been deleted.' % entry.title, 'success')
        return redirect(url_for('entries.index'))

    return render_template('entries/delete.html', entry=entry)
