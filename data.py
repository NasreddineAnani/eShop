import pymysql

def getData():
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()

    cur.execute("SELECT * FROM eShop.products;")

    # print(cur.description)
    # print(cur.description)

    data = cur.fetchall()
    productsData = []

    # print(data)
    for row in data:
        productsData.append({
            'id': row[0],
            'prix': row[1],
            'description': row[2],
            'name': row[3],
            'type': row[4],
            'image': row[5]
        })

    cur.close()
    connection.close()
    return productsData


def getProductData(id):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()

    cur.execute("SELECT * FROM eShop.products WHERE id =" + id + ";")

    data = cur.fetchone()

    # print(data)
    productsData = {
    'id': data[0],
    'prix': data[1],
    'description': data[2],
    'name': data[3],
    'type': data[4],
    'image': data[5]}

    cur.close()
    connection.close()
    return productsData

def addToCart(idCart, idUser, idProduct):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()

    cur.execute("INSERT INTO cart (cartId, userId, prodId) VALUES (" + idCart + "," + idUser + "," + idProduct + ");")

    cur.close()
    connection.close()

def addToCart(idCart, idUser, idProduct):
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="eShop")
    cur = connection.cursor()

    cur.execute("INSERT INTO cart (cartId, userId, prodId) VALUES (" + idCart + "," + idUser + "," + idProduct + ");")

    cur.close()
    connection.close()