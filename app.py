from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import articles
from wtforms import Form, StringField, PasswordField, validators
import pymysql
from passlib.hash import sha256_crypt

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

articles = articles()

connexion = pymysql.connect(host='localhost', user='root', password='mysql', db='eShop')

cursor = connexion.cursor()


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

    name = StringField('Nom', [validators.Regexp('[a-zA-Z ]*$', message="Le nom doit uniquement contenir des lettres et espaces"),
                               validators.Length(min=2, max=50, message="Le nom doit au moins contenir entre 2 et 50 caracteres")])
    email = StringField('Adresse courriel', [validators.Email(message="Cette adresse email est invalide"),
                                             validators.Length(max=100, message="Cette adresse email est trop longue")])

    #ADD REGEX FOR PASSWORD
    password = PasswordField('Mot de passe', [validators.EqualTo('passwordConfirm', message='les mots de passes doivent correspondre')])

    passwordConfirm = PasswordField('Confirmer le mot de passe')

@app.route('/signup', methods=['GET', 'POST'])
def test():
    form = SignUpForm(request.form)

    if request.method == 'POST' and form.validate():

        name = form.name.data

        email = form.email.data

        password = sha256_crypt.encrypt((str(form.password.data)))

        query = "SELECT * FROM users WHERE email = (%s)"

        response = cursor.execute(query, email)

        if int(response) > 0:
            flash("Cette adresse courriel existe deja")
            return render_template('signup.html', form=form)
        else:
            query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, email, password))
            connexion.commit()

            #FLASH FONCTIONNE PAS A REVOIR
            flash("Votre nouveau compte est inscris")

        cursor.close()
        connexion.close()
        session['session_on'] = True
        session['email'] = email
        return redirect('/')

    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

    # try:
    #     request = "select * from test;"
    #
    #     cursor.execute(request)
    #     connexion.commit()
    #
    #     liste = cursor.fetchall()
    # except Exception as e:
    #     print(e)
    #     #handle exeception here
    #
    # response = 'test'
    # for tuple in liste:
    #     response = tuple
    #     for att in tuple:
    #         print(att)
    #     print('\n')
    #
    # cursor.close()
    # connexion.close()