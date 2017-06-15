
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from app import app, db
from models import Entry, Tag, Person

#class EntryModelView(ModelView):
#   column_list = [ 'title', 'status', 'author', 'tease', 'tag_list', 'created_timestamp', ]
#   column_select_related_list = ['author']


class EntryModelView(ModelView):
   _status_choices = [(choice, label) for choice, label in [
     (Entry.STATUS_PUBLIC, 'Public'),
     (Entry.STATUS_DRAFT, 'Draft'),
     (Entry.STATUS_DELETED, 'Deleted'),
   ]]

   column_choices = {
     'status': _status_choices,
   }

   column_filters = [
     'status', Person.name, Person.email, 'created_timestamp'
   ]

   column_list = [
     'title', 'status', 'author', 'tease', 'tag_list', 'created_timestamp',
   ]

   column_searchable_list = ['title', 'status', 'body']
   column_select_related_list = ['author']

admin = Admin(app, 'Blog Admin')
admin.add_view(EntryModelView(Entry, db.session))
admin.add_view(ModelView(Tag, db.session))

class PersonModelView(ModelView):
    column_list = ['email', 'name', 'active', 'created_timestamp']

admin.add_view(PersonModelView(Person, db.session))
