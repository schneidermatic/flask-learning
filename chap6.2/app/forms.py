import wtforms
from wtforms import validators
from models import Person

class LoginForm(wtforms.Form):
    email = wtforms.StringField("Email", validators=[validators.DataRequired()])
    password = wtforms.PasswordField("Password", validators=[validators.DataRequired()])
    remember_me = wtforms.BooleanField("Rember me?",default=True)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False

        self.user = Person.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append("Invalid email or password.")
            return False

        return True
