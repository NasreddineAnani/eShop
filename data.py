import pymysql

def getData():
    connection = pymysql.connect(user="root", passwd="mysql", host="127.0.0.1", port=3306, database="Eshop")
    cur = connection.cursor()

    cur.execute("SELECT * FROM Eshop.products;")

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
