# Form for registering recipes
class InsertForm(Form):
    
    R_name = TextField('name', [validators.Length(min=1, max=35) ,
        validators.Required()])
    R_serve = TextField('servings', [validators.Length(min=1, max=5) ,
            validators.Required(),])    
    R_time = TextField('time', [validators.Length(min=1, max=20), 
            validators.Required(),])    
    Procedure = TextAreaField()
    
# Form for logining in
class LoginForm(Form):
    
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Required(),
    ])
# Form for Registering
class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.Required()])

# user class
class User(UserMixin):
    def __init__(self, name, id, active=True):
        self.name = name
        self.id = id
        self.active = active
 
    def is_active(self):
        return self.active