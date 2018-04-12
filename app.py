from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import getData, getProductData, getCartProduct
import pymysql
from passlib.hash import sha256_crypt
from functools import wraps
from forms import SignUpForm, LoginForm, PriceForm

app = Flask(__name__)

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

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


@app.route('/products', methods=['GET', 'POST'])
def products():
    query = 'SELECT DISTINCT type FROM products;'
    cursor = connexion.cursor()
    cursor.execute(query)
    connexion.commit()
    cursor.close()
    data = cursor.fetchall()
    categories = []
    for row in data:
        categories.append(row[0])
    return render_template('categories.html', categories=categories)


@app.route('/products/category/<string:category>/', methods=['GET', 'POST'])
def category(category):
    unordered_products = getData(category)
    form = PriceForm(request.form)
    data = []

    if request.method == 'POST' and form.validate():
        min = form.minPrice.data
        max = form.maxPrice.data
        order = form.priceOrder.data

        if min is None and max is None:
            if order == 'ASC':
                query = "SELECT * FROM `products` WHERE `type` LIKE (%s) ORDER BY `price` ASC;"
            else:
                query = "SELECT * FROM `products` WHERE `type` LIKE (%s) ORDER BY `price` DESC;"
            cursor = connexion.cursor()
            cursor.execute(query, category)
            connexion.commit()
            cursor.close()
            data = cursor.fetchall()

        elif min is None:
            if order == 'ASC':
                query = "SELECT * FROM products WHERE type LIKE (%s) AND `price` < (%s) ORDER BY price ASC;"
            else:
                query = "SELECT * FROM products WHERE type LIKE (%s) AND `price` < (%s) ORDER BY price DESC;"
            cursor = connexion.cursor()
            cursor.execute(query, (category, max))
            connexion.commit()
            cursor.close()
            data = cursor.fetchall()

        elif max is None:
            if order == 'ASC':
                query = "SELECT * FROM products WHERE type LIKE (%s) AND price > (%s) ORDER BY price ASC;"
            else:
                query = "SELECT * FROM products WHERE type LIKE (%s) AND price > (%s) ORDER BY price DESC;"

            cursor = connexion.cursor()
            cursor.execute(query, (category, min))
            connexion.commit()
            cursor.close()
            data = cursor.fetchall()

        elif min >= max:
            flash('La valeur minimum doit etre inferieur au maximum', category='warning')
            render_template('products.html', Articles=unordered_products, form=form)

        else:
            if order == 'ASC':
                query = "SELECT * FROM products WHERE type LIKE (%s) AND price BETWEEN (%s) AND (%s) ORDER BY price ASC;"
            else:
                query = "SELECT * FROM products WHERE type LIKE (%s) AND price BETWEEN (%s) AND (%s) ORDER BY price DESC;"
            cursor = connexion.cursor()
            cursor.execute(query, (category, min, max))
            connexion.commit()
            cursor.close()
            data = cursor.fetchall()


        productsData = []

        for row in data:
            productsData.append({
                'id': row[0],
                'prix': row[1],
                'description': row[2],
                'name': row[3],
                'category': row[4],
                'image': row[5]
            })
        products = productsData
        return render_template('products.html', Articles=products, form=form, category=category)
    return render_template('products.html', Articles=unordered_products, form=form, category=category)


@app.route('/products/<string:id>/')
def article(id):
    return render_template('article.html', product=getProductData(id))


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

        query = "SELECT * FROM users WHERE email LIKE (%s)"

        response = cursor.execute(query, email)
        connexion.commit()
        cursor.close()

        if int(response) > 0:
            flash("Cette adresse courriel existe deja", category='warning')

            return render_template('signup.html', form=form)

        else:
            cursor = connexion.cursor()
            query = "INSERT INTO users (email, password) VALUES ( %s, %s)"
            cursor.execute(query, (email, password))
            connexion.commit()
            userId = cursor.lastrowid
            cursor.close()

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

        query = "SELECT * FROM users WHERE email LIKE (%s)"
        response = cursor.execute(query, email)

        if int(response) == 0:
            flash("L'utilisateur n'existe pas ou le mot de passe ne correspond pas", category='warning')
            cursor.close()
            return render_template('login.html', form=form)

        else:

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


@app.route("/cart")
@checkLoginForAccess
def cart():
    return render_template('cart.html', cartProduct=getCartProduct(session['idUser']))


if __name__ == '__main__':
    app.run(debug=True)
