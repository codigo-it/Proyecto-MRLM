import mysql.connector
from mysql.connector import errorcode

class dbConnection:
    def __init__(self,user='root',password='',hostIP='127.0.0.1',dbname='test'):
        self.user=user
        self.password=password
        self.hostIP=hostIP
        self.dbname=dbname

    def connect(self):
        try:
            self.cnx = mysql.connector.connect(self.user,self.password,self.hostIP)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Problemas con nombre de usuario o contraseña")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database no existe")
            else:
                print("Error al conectar a DB.\nInfo:\n{}".format(err))
                self.cnx.close()


    def createDB(self):
        cursor = self.cnx.cursor()
        try:
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        except mysql.connector.Error as err:
            print("No se pudo crear DB. Info:\n{}".format(err))




#Si se pudo conectar a mysql, conectarse a database arbitraria

cursor = cnx.cursor()


try:
    cnx.database = DB_NAME  
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

#Si pudo conecctarse a database, crear una tabla nueva
statement1=(
    "CREATE TABLE `empleados` ("
    "  `n_empl` int(11) NOT NULL AUTO_INCREMENT,"
    "  `fecha_nac` date NOT NULL,"
    "  `nombre` varchar(14) NOT NULL,"
    "  `apellido` varchar(16) NOT NULL,"
    "  `genero` enum('M','F') NOT NULL,"
    "  `fecha_contr` date NOT NULL,"
    "  PRIMARY KEY (`n_empl`)"
    ") ENGINE=InnoDB")

try:
    print("Ejecutando statement 1: Creacion de nueva tabla empleados")
    cursor.execute(statement1)
except mysql.connector.Error as err:
    if err.errno ==errorcode.ER_TABLE_EXISTS_ERROR:
        print("La tabla ya existe")
    else:
        print(err.msg)    
else:
    print("OK")


