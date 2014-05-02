
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from wtforms import Form, BooleanField, TextField, PasswordField, validators
app = Flask(__name__)




class RegistrationForm(Form):
    
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('Password', [
        validators.Required(),
    ])


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.email.data,
                        form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)