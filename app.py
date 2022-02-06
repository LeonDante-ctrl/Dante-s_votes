from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisnotsupposedtobepublic'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///home/dante/Documents/Dantes_votes'
Bootstrap(app)
db = SQLAlchemy(app)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me ;)')
class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Thats not right'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])    


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form = form)

@app.route('/signup')
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created successfully</h1>'
    return render_template('signup.html', form = form)

@app.route('/dashboard')
def dashboard():
    return render_template('dash.html')

if __name__ == '__main__':
    app.run(debug=True)