from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import getData, getProductData, getCartProduct, addToCart, deleteToCart, connectDB
import pymysql
from passlib.hash import sha256_crypt
from functools import wraps
from forms import SignUpForm, LoginForm, PriceForm

app = Flask(__name__)

# cle géneré par os.urandom
app.secret_key = b'{\xcd\xb6>\xf2\x02\xcc\x97\xefR\xae\xfflV\x172\x8bA\xf4e\x93\xd5p\xca'
app.config['SESSION_TYPE'] = 'filesystem'

app.jinja_env.globals.update(addProductToCart=addToCart)


# connection a la base de données, changer le mot de passe au besoin
connexion = connectDB()


# décorateur qui restrict l'acces a une page si le user n'est pas connecté
def checkLoginForAccess(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'session_on' in session and session['session_on']:
            return f(*args, **kwargs)
        else:
            flash("Veuillez d'abord vous connecter", 'danger')
            return redirect('/login')

    return wrap


# Page d'acceuil
@app.route('/')
def index():
    return render_template('home.html')


# page de choix des categories
@app.route('/products', methods=['GET', 'POST'])
def products():
    # fetch les categories des produits
    query = 'SELECT DISTINCT category FROM products;'
    cursor = connexion.cursor()
    cursor.execute(query)
    connexion.commit()
    cursor.close()
    data = cursor.fetchall()
    categories = []
    for row in data:
        categories.append(row[0])

    # envoie la liste des categories a la page catogories.html
    return render_template('categories.html', categories=categories)


# Page de recherche des produits classés par categories
@app.route('/products/category/<string:category>/', methods=['GET', 'POST'])
def category(category):
    # fetch tous les produits de la categorie
    unordered_products = getData(category)
    form = PriceForm(request.form)
    data = []

    # traitement quand la page envoie une requete POST pour trier les produits
    if request.method == 'POST' and form.validate():
        min = form.minPrice.data
        max = form.maxPrice.data
        order = form.priceOrder.data

        # quand l'utilisateur ne specifie pas de min ou max
        if min is None and max is None:
            if order == 'ASC':
                query = "SELECT * FROM `products` WHERE `category` LIKE (%s) ORDER BY `price` ASC;"
            else:
                query = "SELECT * FROM `products` WHERE `category` LIKE (%s) ORDER BY `price` DESC;"
            cursor = connexion.cursor()
            cursor.execute(query, category)
            connexion.commit()
            cursor.close()
            data = cursor.fetchall()

        # quand le user specifie seulement un max
        elif min is None:
            if order == 'ASC':
                query = "SELECT * FROM products WHERE category LIKE (%s) AND `price` < (%s) ORDER BY price ASC;"
            else:
                query = "SELECT * FROM products WHERE category LIKE (%s) AND `price` < (%s) ORDER BY price DESC;"
            cursor = connexion.cursor()
            cursor.execute(query, (category, max))
            connexion.commit()
            cursor.close()
            data = cursor.fetchall()

        # quand le user specifie seulement un max
        elif max is None:
            if order == 'ASC':
                query = "SELECT * FROM products WHERE category LIKE (%s) AND price > (%s) ORDER BY price ASC;"
            else:
                query = "SELECT * FROM products WHERE category LIKE (%s) AND price > (%s) ORDER BY price DESC;"

            cursor = connexion.cursor()
            cursor.execute(query, (category, min))
            connexion.commit()
            cursor.close()
            data = cursor.fetchall()

        elif min >= max:
            flash('La valeur minimum doit etre inferieur au maximum', category='warning')
            render_template('products.html', Articles=unordered_products, form=form)

        # quand le min et le max sont specifiés
        else:
            if order == 'ASC':
                query = "SELECT * FROM products WHERE category LIKE (%s) AND price BETWEEN (%s) AND (%s) ORDER BY price ASC;"
            else:
                query = "SELECT * FROM products WHERE category LIKE (%s) AND price BETWEEN (%s) AND (%s) ORDER BY price DESC;"
            cursor = connexion.cursor()
            cursor.execute(query, (category, min, max))
            connexion.commit()
            cursor.close()
            data = cursor.fetchall()

        productsData = []

        for row in data:
            productsData.append({
                'idProduct': row[0],
                'prix': row[1],
                'description': row[2],
                'name': row[3],
                'category': row[4],
                'image': row[5]
            })
        products = productsData

        return render_template('products.html', products=products, form=form, category=category)
    return render_template('products.html', products=unordered_products, form=form, category=category)


@app.route('/products/category/<string:category>/<string:id>/', methods=['GET', 'POST'])
@checkLoginForAccess
def product(id, category):
    if request.method == 'POST':
        boolAddedToCart = addToCart(session['idUser'], id, request.form['quantity'])
        if (boolAddedToCart):
            flash('Produit ajouter à votre panier', category='info')
            return redirect('/products/category/' + str(category) + '/' + str(id) + '/')
        else:
            flash('Le produit est déjà présent dans votre panier', category='warning')
            return redirect('/products/category/' + str(category) + '/' + str(id) + '/')

    return render_template('product.html', product=getProductData(id), userId=session['idUser'])


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # dans le cas ou l'utilisateur accede par l'url /signup en etant connecté
    if 'session_on' in session and session['session_on']:
        flash('Deconnectez vous pour inscrire un nouveau compte', category='info')
        return redirect('/')

    # formulaire WTForm
    form = SignUpForm(request.form)
    cursor = connexion.cursor()

    # envoie du formulaire
    if request.method == 'POST' and form.validate():

        email = form.email.data

        # encryption du mot de passe
        password = sha256_crypt.encrypt((str(form.password.data)))

        query = "SELECT * FROM users WHERE email LIKE (%s)"

        response = cursor.execute(query, email)
        connexion.commit()
        cursor.close()

        # verifie si le courriel existe deja
        if int(response) > 0:
            flash("Cette adresse courriel existe deja", category='warning')

            return render_template('signup.html', form=form)

        # creation du nouveau compte
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

        # si le email n'existe pas, la reponse est vide
        if int(response) == 0:
            flash("L'utilisateur n'existe pas ou le mot de passe ne correspond pas", category='warning')
            cursor.close()
            return render_template('login.html', form=form)

        else:

            response = cursor.fetchone()

            hashedpwd = response[2]

            userId = response[0]

            password = form.password.data

            # verifie que le mot de passe correspond au hash stocké dans la base de données
            if sha256_crypt.verify(password, hashedpwd):
                flash("Vous etes connecté", category='success')
                session['session_on'] = True
                session['email'] = email
                session['idUser'] = userId
                cursor.close()
                return redirect('/')

            # cas ou le mot de passe est faux
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
    if request.method == 'POST':
        boolIsInCart = deleteToCart(session['idUser'], int(request.form['idProduct']))
        if (boolIsInCart):
            flash('Produit retirer à votre panier', category='info')
            return redirect('/cart')
        else:
            flash("Le produit n'est pas présent dans votre panier", category='warning')
            return redirect('/cart')
    return render_template('cart.html', cartProduct=getCartProduct(session['idUser']))


if __name__ == '__main__':
    app.run(debug=True)
