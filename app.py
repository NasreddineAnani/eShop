from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import articles
from wtforms import Form, StringField, PasswordField, validators
import pymysql
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

articles = articles()

connexion = pymysql.connect(host='localhost', user='root', password='mysql', db='eShop')


# Index
@app.route('/')
def index():
    return render_template('home.html')


@app.route('/products')
def products():
    return render_template('products.html', Articles=articles)


@app.route('/products/<string:id>/')
def article(id):
    return render_template('article.html', id=id)


class SignUpForm(Form):
    email = StringField('Adresse courriel', [validators.Email(message="Cette adresse email est invalide"),
                                             validators.Length(max=100, message="Cette adresse email est trop longue")])

    # ADD REGEX FOR PASSWORD
    password = PasswordField('Mot de passe',
                             [validators.EqualTo('passwordConfirm', message='les mots de passes doivent correspondre')])

    passwordConfirm = PasswordField('Confirmer le mot de passe')


class LoginForm(Form):
    email = StringField('Adresse courriel', [validators.data_required(message='Ce champ doit etre remplis')])
    password = PasswordField('Mot de passe', [validators.data_required(message='Ce champ doit etre remplis')])


@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if session['session_on']:
        flash('Deconnectez vous pour inscrire un nouveau compte', category='info')
        return redirect('/')

    form = SignUpForm(request.form)
    cursor = connexion.cursor()

    if request.method == 'POST' and form.validate():

        email = form.email.data

        password = sha256_crypt.encrypt((str(form.password.data)))

        query = "SELECT * FROM users WHERE email = (%s)"

        response = cursor.execute(query, email)

        if int(response) > 0:
            flash("Cette adresse courriel existe deja", category='warning')
            cursor.close()

            return render_template('signup.html', form=form)
        else:
            query = "INSERT INTO users (email, password) VALUES ( %s, %s)"
            cursor.execute(query, (email, password))
            connexion.commit()

            flash("Votre nouveau compte est inscris", category='success')
            cursor.close()

        session['session_on'] = True
        session['email'] = email
        return redirect('/')

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    cursor = connexion.cursor()

    if request.method == 'POST':

        email = form.email.data

        query = "SELECT * FROM users WHERE email = (%s)"
        response = cursor.execute(query, email)

        if int(response) == 0:
            flash("L'utilisateur n'existe pas ou le mot de passe ne correspond pas", category='warning')
            cursor.close()
            return render_template('login.html', form=form)

        else:
            pwdQuery = "SELECT * FROM users WHERE email = (%s)"

            cursor.execute(pwdQuery, email)

            hashedpwd = cursor.fetchone()[2]

            password = form.password.data

            if sha256_crypt.verify(password, hashedpwd):
                flash("Vous etes connecté", category='success')
                session['session_on'] = True
                session['email'] = email
                cursor.close()
                return redirect('/')

            else:
                flash("L'utilisateur n'existe pas ou le mot de passe ne correspond pas", category='warning')
                cursor.close()
                return render_template('login.html', form=form)

    return render_template('login.html', form=form)


def checkLoginForAccess(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'session_on' in session:
            return f(*args, **kwargs)
        else:
            flash("Veuillez d'abord vous connecter", 'danger')
            return redirect('/login')

    return wrap


@app.route("/logout")
@checkLoginForAccess
def logout():
    session.clear()
    flash('Vous avez été deconnecté', category='success')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
