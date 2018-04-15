import pymysql

file = open("sqlData.txt", 'r')
lines = file.readlines()
file.close()

connexion = pymysql.connect(host="localhost", user="root", password="mysql")
cursor = connexion.cursor()

query1 = 'CREATE DATABASE eShop;'
query2 = 'USE eShop;'
query3 = 'CREATE TABLE eShop.products (`idProduct` INT UNSIGNED NOT NULL AUTO_INCREMENT, `price` FLOAT NOT NULL, `description` TEXT NOT NULL, `name` VARCHAR(45) NOT NULL, `category` VARCHAR(45) NOT NULL, `imgUrl` TEXT NOT NULL,  `quantity` INT UNSIGNED NOT NULL,  PRIMARY KEY (`idProduct`));'
query4 = 'CREATE TABLE users (userId INT UNSIGNED NOT NULL AUTO_INCREMENT, email VARCHAR(100) NOT NULL, password varchar(100) NOT NULL, PRIMARY KEY(userId));'
query5 = 'CREATE TABLE cart (userId INT UNSIGNED NOT NULL, idProduct INT UNSIGNED, quantityInCart INT UNSIGNED NOT NULL, PRIMARY KEY (userId, idProduct), FOREIGN KEY (userId) REFERENCES users(userId) ON UPDATE CASCADE, FOREIGN KEY (idProduct) REFERENCES products(idProduct) ON UPDATE CASCADE);'
query6 = 'CREATE INDEX prices USING BTREE ON products (category, price);'
query7 = 'CREATE UNIQUE INDEX login USING HASH ON users (email);'
query8 = 'CREATE INDEX cartIndex USING HASH ON cart (userId);'

cursor.execute(query1)
cursor.execute(query2)
cursor.execute(query3)
cursor.execute(query4)
cursor.execute(query5)
cursor.execute(query6)
cursor.execute(query7)
cursor.execute(query8)
connexion.commit()

cursor.close()
connexion.close()

db2 = pymysql.connect(host="localhost", user="root", password="mysql", db="eShop")
cursor2 = db2.cursor()

for line in lines:
    cursor2.execute(str(line))
    db2.commit()

cursor2.close()
db2.close()
