import pymysql

# Cette methode permet de se connecter a la base de donnee
def connectDB():
    return pymysql.connect(host='localhost', user='root', password='UnAutreMotDePasse', db='eShop')

# Cette methode permet d`aller chercher les informations de tous articles d`une categorie en particulier dans la table products
def getData(category):
    connection = connectDB()
    cur = connection.cursor()

    # selectionne tous les produits avec la categorie spécifié
    cur.execute("SELECT * FROM eShop.products WHERE category LIKE (%s);", category)

    data = cur.fetchall()
    productsData = []

    # print(data)
    for row in data:
        # creation dun vecteur avec des tuples de produit
        productsData.append({
            'idProduct': row[0],
            'prix': row[1],
            'description': row[2],
            'name': row[3],
            'category': row[4],
            'image': row[5],
            'qty': row[6],
        })

    cur.close()
    connection.close()
    return productsData

# Cette methode permet d`aller chercher les informations d`un article en particulier dans la table products
def getProductData(id):
    connection = connectDB()
    cur = connection.cursor()

    # selection d'un produit selon son ID
    cur.execute("SELECT * FROM eShop.products WHERE idProduct =(%s);", id)

    data = cur.fetchone()

    # print(data)
    productsData = {
        'idProduct': data[0],
        'prix': data[1],
        'description': data[2],
        'name': data[3],
        'category': data[4],
        'image': data[5],
        'qty': data[6], }

    cur.close()
    connection.close()
    return productsData

# Cette methode permet d`aller ajouter un article dans le panier d`achat de l`utilisateur
def addToCart(idUser, idProduct, quantityInCart):
    connection = connectDB()
    cur = connection.cursor()
    cur.execute("SELECT * FROM eShop.cart WHERE userId = %s AND idProduct = %s", [str(idUser), str(idProduct)])
    if cur.rowcount == 0:
        cur.execute("INSERT INTO eShop.cart (userId, idProduct, quantityInCart) VALUES ( %s, %s, %s);",
                    [str(idUser), str(idProduct), str(quantityInCart)])
        connection.commit()
        return True
    else:
        return False
    cur.close()
    connection.close()

# Cette methode permet d`aller retirer un article contenu dans le panier d`achat de l`utilisateur
def deleteToCart(idUser, idProduct):
    connection = connectDB()
    cur = connection.cursor()
    cur.execute("SELECT * FROM eShop.cart WHERE userId = %s AND idProduct = %s", [str(idUser), str(idProduct)])
    if cur.rowcount > 0:
        cur.execute("DELETE FROM eShop.cart WHERE userId = %s AND idProduct = %s", [str(idUser), str(idProduct)])
        connection.commit()
        return True
    else:
        return False
    cur.close()
    connection.close()

# Cette methode permet d`aller chercher les articles dans le panier d`achat de l`utilisateur
# Pour cela, la methode effectue une jointure entre la table cart et products en fonction des products id dans le panier d`achat
def getCartProduct(idUser):
    connection = connectDB()
    cur = connection.cursor()
    cur.execute(
        "SELECT products.idProduct, products.price, products.description, products.name, products.category, products.imgUrl, cart.quantityInCart FROM products INNER JOIN cart ON products.idProduct = cart.idProduct WHERE cart.userId = (%s);",
        idUser)
    data = cur.fetchall()
    productsData = []

    # print(data)
    for row in data:
        productsData.append({
            'idProduct': row[0],
            'prix': row[1],
            'description': row[2],
            'name': row[3],
            'category': row[4],
            'image': row[5],
            'qty': row[6],
            'idUser': idUser
        })

    cur.close()
    connection.close()

    return productsData
