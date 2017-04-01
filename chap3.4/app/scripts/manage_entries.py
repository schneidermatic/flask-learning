import os, sys
sys.path.append(os.getcwd())

from main import db
from models import *

entries = [
           Entry(title='Python entry', body='This is a post about Python'),
           Entry(title='Flask entry', body='This is a post about Flask'),
           Entry(title='More Flask', body='This is a post about More Flask'),
           Entry(title='Django entry', body='This is a post about Django')
          ]

tags = [
         Tag(name='python'),
         Tag(name='flask')
       ]

if __name__ == '__main__':
    #for entry in [Entry.query.all(),Tag.query.all()]:
    #    print(entry)
    #    try:
    #      db.session.delete(entry) 
    #      db.session.commit() 
    #    except: 
    #      pass

    for entry in (entries):
        db.session.add(entry)
        db.session.commit()

    #python_entry = Entry.query.filter(Entry.title == 'Python entry').all()
    #flask_entry  = Entry.query.filter(Entry.title == 'Flask entry').all()

    #python_entry.tags = tags
    #flask_entry.tags  = [tags[1]]

    db.session.commit()
