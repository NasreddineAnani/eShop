import pymysql

file = open("sqlData.txt", 'r')
lines = file.readlines()
file.close()

db1 = pymysql.connect(host="localhost",user="root",password="mysql")
cursor = db1.cursor()

query1 = 'CREATE DATABASE eShop;'
query2 = 'USE eShop;'
query3 = 'CREATE TABLE `products` (`idProduct` INT UNSIGNED NOT NULL, `price` FLOAT NOT NULL, `description` MEDIUMTEXT NOT NULL, `name` VARCHAR(45) NOT NULL, `type` VARCHAR(45) NOT NULL, `imgUrl` MEDIUMTEXT NOT NULL,   PRIMARY KEY (`idProduct`));'
query4 = 'CREATE TABLE users (id INT(11) AUTO_INCREMENT PRIMARY KEY, email VARCHAR(100), password varchar(100));'
query5 = 'CREATE TABLE cart (userId INT(11) NOT NULL, prodId INT(11));'

cursor.execute(query1)
cursor.execute(query2)
cursor.execute(query3)
cursor.execute(query4)

cursor.close()
db1.close()

db2 = pymysql.connect(host="localhost", user="root", password="mysql", db="eShop")
cursor2 = db2.cursor()

for line in lines:
    print(line)
    cursor2.execute(str(line))
    db2.commit()

cursor2.close()
db2.close()
