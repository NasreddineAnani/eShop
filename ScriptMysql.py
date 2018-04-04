import pymysql

file = open("sqlData.txt", 'r')
lines = file.readlines()
file.close()

db1 = pymysql.connect(host="localhost",user="root",password="mysql")
cursor = db1.cursor()

# query1 = 'CREATE DATABASE test18;'
# query2 = 'USE test18;'
# query3 = 'CREATE TABLE `test18` (`idProduct` INT UNSIGNED NOT NULL, `price` FLOAT NOT NULL, `description` MEDIUMTEXT NOT NULL, `name` VARCHAR(45) NOT NULL, `type` VARCHAR(45) NOT NULL, `imgUrl` MEDIUMTEXT NOT NULL,   PRIMARY KEY (`idProduct`));'
#
# cursor.execute(query1)
# cursor.execute(query2)
# cursor.execute(query3)
cursor.close()
db1.close()

db2 = pymysql.connect(host="localhost", user="root", password="mysql", db="test18")
cursor2 = db2.cursor()
# query = "INSERT INTO test18 (idProduct, price, description, name, type, imgUrl) VALUES (1, 1759.89, 'Sometimes water boy want within.', 'Scott Marshall and Sullivan', 'hawaii', 'https://images.unsplash.com/photo-1466501802958-fa215d854df3?ixlib=rb-0.3.5&ixidProduct=eyJhcHBfaWQiOjEyMDd9&s=fb13603c544d540da9117097b2473d20&auto=format&fit=crop&w=440');"
# print(query)
# cursor2.execute(query)
# db2.commit()

for line in lines:
    print(line)
    cursor2.execute(str(line))
    db2.commit()

cursor2.close()
db2.close()
