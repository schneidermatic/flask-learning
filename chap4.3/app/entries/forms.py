import wtforms

from wtforms.validators import DataRequired
from models import Entry
from models import Tag
from app import app
from app import db

class TagField(wtforms.StringField):
    def _value(self):
        if self.data:
            #Display tags as a comma-separated list.
            return ', '.join([tag.name for tag in self.data])
        return ''

    def get_tags_from_string(self, tag_string):
        raw_tags = tag_string.split(',')
        # Filter out any empty tag names.
        tag_names = [name.strip() for name in raw_tags if name.strip()]
        app.logger.info("--/-> tags")
        app.logger.info(tag_names)
        # Query the database and retrieve any tags we have already saved.
        existing_tags = Tag.query.filter(Tag.name.in_(tag_names))
        #existing_tags = Tag.query.filter(Tag.name == 'Python')
        #existing_tags = db.session.query(Tag).filter(Tag.name.in_(tag_names))
        for tag in existing_tags:
            app.logger.info("--//->" + str(tag.name))

        app.logger.info(existing_tags)
        # Determine which tag names are new.
        new_names = set(tag_names) - set([tag.name for tag in existing_tags])

        for new_name in new_names:
            app.logger.info("--///->" + str(new_name))

        # Create a list of unsaved Tag instances for the new tags.
        new_tags = [Tag(name=name) for name in new_names]
        # Return all the exiting tags + all the new, unsaved tags.
        return list(existing_tags) + new_tags

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = self.get_tags_from_string(valuelist[0])
        else:
            self.data = []

class EntryForm(wtforms.Form):
    title = wtforms.StringField('Title', validators=[DataRequired()])
    body = wtforms.TextAreaField('Body', validators=[DataRequired()])
    status = wtforms.SelectField(
        'Entry status',
        choices=(
            (Entry.STATUS_PUBLIC, 'Public'),
            (Entry.STATUS_DRAFT, 'Draft')),
        coerce=int)
    tags = TagField('Tags', description='Separate multiple tags with commas.')

    def save_entry(self, entry):
        self.populate_obj(entry)
        
        for tag in entry.tags:
            app.logger.info("___>" + str(tag.name))

        entry.generate_slug()
        return entry
