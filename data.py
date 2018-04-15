import pymysql

def getData(category):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()

    cur.execute("SELECT * FROM eShop.products WHERE category LIKE (%s);", category)

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
        })

    cur.close()
    connection.close()
    return productsData


def getProductData(id):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()

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
    'qty': data[6],}

    cur.close()
    connection.close()
    return productsData

def addToCart(idUser, idProduct, quantityInCart):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()
    cur.execute("SELECT * FROM eShop.cart WHERE userId = %s AND idProduct = %s", [str(idUser), str(idProduct)])
    if cur.rowcount == 0:
        cur.execute("INSERT INTO eShop.cart (userId, idProduct, quantityInCart) VALUES ( %s, %s, %s);", [str(idUser), str(idProduct), str(quantityInCart)])
        connection.commit()
        return True
    else:
        return False
    cur.close()
    connection.close()

def deleteToCart(idUser, idProduct):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
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
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()
    cur.execute("SELECT * FROM products INNER JOIN cart ON products.idProduct = cart.idProduct WHERE cart.userId = (%s);",idUser)
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
