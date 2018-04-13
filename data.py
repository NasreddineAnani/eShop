import pymysql

def getData(type):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()

    cur.execute("SELECT * FROM eShop.products WHERE type LIKE (%s);", type)

    data = cur.fetchall()
    productsData = []

    # print(data)
    for row in data:
        productsData.append({
            'idProduct': row[0],
            'prix': row[1],
            'description': row[2],
            'name': row[3],
            'type': row[4],
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
    'type': data[4],
    'image': data[5],
    'qty': data[6],}

    cur.close()
    connection.close()
    return productsData

def addToCart(idUser, idProduct):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()
    cur.execute("SELECT * FROM eShop.cart WHERE userId = %s AND prodId = %s", [str(idUser), str(idProduct)])
    if cur.rowcount == 0:
        cur.execute("INSERT INTO eShop.cart (userId, prodId) VALUES ( %s, %s);", [str(idUser), str(idProduct)])
        connection.commit()
        return True
    else:
        return False
    cur.close()
    connection.close()

def deleteToCart(idUser, idProduct):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()
    cur.execute("SELECT * FROM eShop.cart WHERE userId = %s AND prodId = %s", [str(idUser), str(idProduct)])
    if cur.rowcount > 0:
        cur.execute("DELETE FROM eShop.cart WHERE userId = %s AND prodId = %s", [str(idUser), str(idProduct)])
        connection.commit()
        return True
    else:
        return False
    cur.close()
    connection.close()

def getCartProduct(idUser):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()
    cur.execute("SELECT * FROM products INNER JOIN cart ON products.idProduct = cart.prodId WHERE cart.userId = (%s);",idUser)
    data = cur.fetchall()
    productsData = []

    # print(data)
    for row in data:
        productsData.append({
            'idProduct': row[0],
            'prix': row[1],
            'description': row[2],
            'name': row[3],
            'type': row[4],
            'image': row[5],
            'qty': row[6],
            'idUser': idUser
        })

    cur.close()
    connection.close()

    return productsData
