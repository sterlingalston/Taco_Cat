from flask import (Flask, g, render_template, flash, redirect, url_for,
                  abort)
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required, current_user)

import forms
import models

#setting up ports and defaults

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'auoesh.bouoastuh.43,uoausoehuosth3ououea.auoub!'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """Close the database connection after each request."""
    g.db.close()
    return response
  
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Yay, you registered!", "success")
        models.User.create_user(
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
'''  
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404 # status code to send back when rendering template  
'''

@app.route('/taco', methods = ('GET', 'POST'))
def taco(): #@login_required
    form = forms.TacoForm()
    if form.validate_on_submit():
        models.Taco.create( user = g.user._get_current_object(),
                           protein = form.protein.data.strip(),
                           shell = form.shell.data.strip(),
                           cheese = form.cheese.data,
                           extras = form.extras.data.strip())
        flash("Message posted! Thanks!", "success")
        return redirect(url_for('index'))
    return render_template('taco.html', form = form)

@app.route('/')
def index():
    tacos = models.Taco.select().limit(100)
    return render_template('index.html', tacos = tacos)
  
if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            email='malston@gmail.com',
            password='malston11',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)