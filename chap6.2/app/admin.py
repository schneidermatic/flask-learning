
from flask.ext.admin import Admin
from flask.ext.admin.contrib.sqla import ModelView

from app import app, db
from models import Entry, Tag, Person
from wtforms.fields import SelectField
from wtforms.fields import PasswordField

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
   form_args = {
        'status': {'choices': _status_choices, 'coerce': int},
   }
   form_columns = ['title', 'body', 'status', 'author', 'tags']
   form_overrides = {'status': SelectField}
   form_ajax_refs = {
       'author': {
          'fields': (Person.name, Person.email),
       },
   }

admin = Admin(app, 'Blog Admin')
admin.add_view(EntryModelView(Entry, db.session))
admin.add_view(ModelView(Tag, db.session))

class PersonModelView(ModelView):
    column_filters = ('email', 'name', 'active')
    column_list = ['email', 'name', 'active', 'created_timestamp']
    column_searchable_list = ['email', 'name']

    form_columns = ['email', 'password', 'name', 'active']
    form_extra_fields = {
        'password': PasswordField('New password'),
    }

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password_hash = Person.make_password(form.password.data)
        return super(PersonModelView, self).on_model_change(form, model, is_created)



admin.add_view(PersonModelView(Person, db.session))
