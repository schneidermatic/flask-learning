from flask import Flask

from config import Configuration # import our config data.

app = Flask(__name__)
app.config.from_object(Configuration) # use values from our config object.
