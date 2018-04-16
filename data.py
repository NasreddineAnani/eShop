import pymysql

def connectDB():
    return pymysql.connect(host='localhost', user='root', password='UnAutreMotDePasse', db='eShop')

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


def getCartProduct(idUser):
    connection = connectDB()
    cur = connection.cursor()
    cur.execute(
        "SELECT * FROM products INNER JOIN cart ON products.idProduct = cart.idProduct WHERE cart.userId = (%s);",
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
            'qty': row[9],
            'idUser': idUser
        })

    cur.close()
    connection.close()

    return productsData
