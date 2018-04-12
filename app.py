
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import getData, getProductData, getCartProduct, addToCart, deleteToCart
from wtforms import Form, StringField, PasswordField, validators
import pymysql
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'


app.jinja_env.globals.update(addProductToCart=addToCart)


def test() :
    return "wesh poto"


app.jinja_env.globals.update(test=test)


articles = getData()

connexion = pymysql.connect(host='localhost', user='root', password='mysql', db='eShop')

def checkLoginForAccess(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'session_on' in session and session['session_on']:
            return f(*args, **kwargs)
        else:
            flash("Veuillez d'abord vous connecter", 'danger')
            return redirect('/login')

    return wrap

# Index
@app.route('/')
def index():

    return render_template('home.html')


@app.route('/products')
def products():
    return render_template('products.html', Articles=articles)


@app.route('/products/<string:id>/', methods=['GET','POST'])
@checkLoginForAccess
def article(id):
    if request.method == 'POST':
        boolAddedToCart = addToCart(session['idUser'], id)
        if (boolAddedToCart):
            flash('Produit ajouter à votre panier', category='info')
            return redirect('/products/' + str(id) + '/')
        else:
            flash('Le produit est déjà présent dans votre panier', category='warning')
            return redirect('/products/' + str(id) + '/')

    return render_template('article.html', product=getProductData(id), userId=session['idUser'], )

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

    if 'session_on' in session and session['session_on']:
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

            query = "SELECT * FROM users WHERE email = (%s)"
            cursor.execute(query, email)
            userId = cursor.fetchone()[0]
            connexion.commit()

            flash("Votre nouveau compte est inscris", category='success')
            cursor.close()

        session['idUser'] = userId
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

            response = cursor.fetchone()

            hashedpwd = response[2]

            userId = response[0]

            password = form.password.data

            if sha256_crypt.verify(password, hashedpwd):
                flash("Vous etes connecté", category='success')
                session['session_on'] = True
                session['email'] = email
                session['idUser'] = userId
                cursor.close()
                return redirect('/')

            else:
                flash("L'utilisateur n'existe pas ou le mot de passe ne correspond pas", category='warning')
                cursor.close()
                return render_template('login.html', form=form)

    return render_template('login.html', form=form)

@app.route("/logout")
@checkLoginForAccess
def logout():
    session['session_on'] = False
    session['email'] = ''
    flash('Vous avez été deconnecté', category='success')
    return redirect('/')

@app.route("/cart", methods=['GET', 'POST'])
@checkLoginForAccess
def cart():
    print("tkt")
    userId = request.form.get('id')
    if request.method == 'POST':
        print("weshmag")
        boolIsInCart = deleteToCart(session['idUser'], int(request.form['id']))
        if (boolIsInCart):
            flash('Produit retirer à votre panier', category='info')
            return redirect('/cart')
        else:
            flash("Le produit n'est pas présent dans votre panier", category='warning')
            return redirect('/cart')
    return render_template('cart.html', cartProduct=getCartProduct(session['idUser']))

##request.headers['your-header-name']



if __name__ == '__main__':
    app.run(debug=True)
