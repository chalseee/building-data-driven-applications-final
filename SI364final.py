import os, json, datetime, api_info, requests
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, TextAreaField
from wtforms import StringField, SubmitField, FileField, PasswordField, BooleanField, SelectMultipleField, ValidationError
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import LoginManager, login_required, logout_user, login_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'secretstringhere'

#postgresql://localhost/YOUR_DATABASE_NAME
#"postgresql://postgres:icedout@localhost:5432/chalseodb"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or "postgresql://localhost/chalseo"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager=Manager(app)
db=SQLAlchemy(app)
migrate=Migrate(app, db)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

#Models
#includes 1-many relationship between words and definitions
#includes many-many relationship betweeen words and partofspeech
pos_word = db.Table('pos_word', db.Column('pos_id', db.Integer, db.ForeignKey('partofspeech.id')), db.Column('word_id', db.Integer, db.ForeignKey('words.id')))

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # user_words = db.relationship('Word', backref="User")

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Word(db.Model):
    __tablename__ = "words"
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(5))
    word = db.Column(db.String(32))
    phonetic_spelling = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pos = db.relationship('PartOfSpeech', secondary=pos_word, backref=db.backref('words', lazy='dynamic'), lazy='dynamic')
    rel = db.relationship("Definition")

class Definition(db.Model):
    __tablename__ = "definitions"
    id = db.Column(db.Integer, primary_key=True)
    definition = db.Column(db.String(264))
    domain = db.Column(db.String(16))
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'))

class PartOfSpeech(db.Model):
    __tablename__ = "partofspeech"
    id = db.Column(db.Integer, primary_key=True)
    part_of_speech = db.Column(db.String(32))

#Form classes will go here
class RegistrationForm(FlaskForm):
    email = StringField('Email:', validators=[Required(),Length(1,64),Email()])
    username = StringField('Username:',validators=[Required(),Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores')])
    password = PasswordField('Password:',validators=[Required(),EqualTo('password2',message="Passwords must match")])
    password2 = PasswordField("Confirm Password:",validators=[Required()])
    submit = SubmitField('Register User')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class WordSearchForm(FlaskForm):
    word = StringField('Word: ', validators=[Required(), Length(1,16)])
    submit = SubmitField()

    def validate_word(self, field):
        if len(field.data.split(' ')) > 1:
            raise ValidationError('Word must be one word!')

class UpdateButtonForm(FlaskForm):
    submit = SubmitField("Update")

class UpdateWordForm(FlaskForm):
    new_language = StringField("What is the new language for this item?", validators=[Required(), Length(1,8)])
    new_ipa = StringField("What is the new pronunciation for this word?", validators=[Required()])
    submit = SubmitField("Update")

    def validate_new_word(self, field):
        if len(field.data.split(' ')) > 1:
            raise ValidationError('New word must be one word!')

class DeleteButtonForm(FlaskForm):
    submit = SubmitField("Delete")

#helper fxns
def oxford_dict_request(app_id, app_key, base_url, word_id):
    base_url = base_url + word_id.lower()
    data = requests.get(base_url, headers={'app_id': app_id, 'app_key':app_key})
    if data:
        return data.json()['results'][0]
    return None

def get_or_create_word(word):
    w = Word.query.filter_by(word=word).first()
    if not w:
        d = oxford_dict_request(api_info.app_id, api_info.app_key, api_info.base_url, word)
        if d is None:
            return None
        w = Word(word=word, language=d['language'], user_id=current_user.id, phonetic_spelling=d['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling'], pos=[])
        db.session.add(w)
        db.session.commit()

        p = get_or_create_pos(w, d['lexicalEntries'][0]['lexicalCategory'])
        get_or_create_definition(w, d['lexicalEntries'][0]['entries'][0]['senses'])

        return w
    return w


def get_or_create_definition(word_obj, definitions):
    for d in definitions:
        tmp = Definition(definition="none available", domain="None", word_id=word_obj.id)
        if 'domains' in d.keys():
            tmp.domain = d['domains'][0]
        if 'definitions' in d.keys():
            tmp.definition=d['definitions']
        db.session.add(tmp)
        db.session.commit()

def get_or_create_pos(word_obj, partofspeech):
    pos = PartOfSpeech.query.filter_by(part_of_speech=partofspeech).first()
    if pos:
        return pos
    else:
        pos = PartOfSpeech(part_of_speech=partofspeech)
        db.session.add(pos)
        db.session.commit()
        return pos


#View functions - all include the base navigation menu
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html',form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now log in!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/secret')
def secret():
    return "Only authenticated users can do this! Try to log in or contact the site admin."

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    form2 = WordSearchForm()

    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))

    return render_template('index.html', form2=form2, form=form)

@app.route('/all_words')
def all_words(): #should render a page that shows information about all words that have been added on this app. it will list all information in the words table.
    words = Word.query.all()
    defs = []
    for w in words:
        d = Definition.query.filter_by(word_id=w.id)
        defs.append((w, d))
    return render_template('all_words.html', words=defs)

@app.route('/your_definitions')
@login_required
def your_definitions(): #should render a page that shows information about all words that have been added on this app. it will list all information in the words table.
    words = Word.query.filter_by(user_id=current_user.id)
    defs = []
    for w in words:
        d = Definition.query.filter_by(word_id=w.id)
        defs.append((w, d))
    return render_template('your_definitions.html', words=defs)

@app.route('/delete/<word_id>', methods=["GET", "POST"])
@login_required
def delete(word_id): #should allow the user to delete a word from their list of words. this will remove the entry from the words table, but not it's associated definition(s). will submit/route to the your_words page.
    word = Word.query.filter_by(id=word_id).first()
    definitions = Definition.query.filter_by(word_id=word_id)
    for d in definitions:
        db.session.delete(d)
    db.session.delete(word)
    db.session.commit()
    flash('Successfully deleted word: ' + word.word)
    return redirect(url_for('your_words'))

@app.route('/update/<word_id>', methods=["GET", "POST"])
@login_required
def update(word_id): #should allow the user to change a word from their list of words and then run a get_or_create fxn to update possible new parts of speech or definition(s). will submit/route to the your_words page.
    word = Word.query.filter_by(id=word_id).first()
    form = UpdateWordForm()
    if form.validate_on_submit():
        word.language = form.new_language.data
        word.phonetic_spelling = form.new_ipa.data
        db.session.commit()
        flash("Updated priority of item: " + word.word + "!")
        return redirect(url_for('your_words'))
    return render_template('update.html', word=word, form=form) #page requires login

@app.route('/your_words', methods=["GET", "POST"])
@login_required
def your_words(): #displays all words that the user has added to their collection. also displays a form to enter a word. page will update to show this word in addition to all past ones once the form is submitted correctly. otherwise, it will still redirect to this page, but flash an error message
    if request.args:
        print('WORKING')
        word = request.args['word']
        result = get_or_create_word(word)
        if result == None:
            flash('Invalid query. Try again.')
            return redirect(url_for('index'))

    words = Word.query.filter_by(user_id=current_user.id)
    return render_template('your_words.html', words=words, form=DeleteButtonForm(), form2=UpdateButtonForm())


if __name__ == "__main__":
    db.create_all()
    manager.run()
