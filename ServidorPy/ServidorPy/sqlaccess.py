"""Modulo que contiene la clase dbConnection para acceder a database mysql"""
import logging
import mysql.connector
from mysql.connector import errorcode

class DBConnection:
    """Clase para usar el python-MySQL connector """

    def __init__(self,
                 user='root',
                 password='',
                 hostIP='127.0.0.1',
                 dbname='none',
                 autocommit=True):
        """Constructor inicializa los atributos basicos"""
        self.logger = logging.getLogger()
        self.user = user
        self.password = password
        self.host_ip = hostIP
        self.dbname = dbname
        self.autocommit = autocommit
        self.cnx = None

    def connect(self):
        """Establecer conexion con el servidor mysql"""

        try:
            self.cnx = mysql.connector.connect(user=self.user,
                                               password=self.password,
                                               host=self.host_ip,
                                               autocommit=self.autocommit)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.logger.error("Problemas con nombre de usuario o contraseña")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.logger.error("Database no existe")
            else:
                self.logger.error("Error al conectar a DB.\nInfo:\n{}".format(err))
                self.cnx.close()
                return 1
        if self.dbname != 'none':
            self.cnx.database = self.dbname
            return 0

    def create_db(self):
        """Crea una nueva base de datos en el servidor mysql"""

        cursor = self.cnx.cursor()
        try:
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self.dbname))
        except mysql.connector.Error as err:
            self.logger.error("No se pudo crear DB. Info:\n{}".format(err))
        else:
            cursor.close()

    #Esqueleto de funcion CreateTable, no funcional (valga la redundancia).
    def create_table(self, tablename='default'):
        """Crea una tabla nueva"""
        cursor = self.cnx.cursor()
        try:
            self.cnx.database = self.dbname
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_db()
                self.cnx.database = self.dbname
            else:
                print(err)
                return 1

        #Si pudo conectarse a database, crear una tabla nueva.
        statement1 = (
                      "CREATE TABLE `default` ("
                      "  `n_empl` int(11) NOT NULL AUTO_INCREMENT,"
                      "  `fecha_nac` date NOT NULL,"
                      "  `nombre` varchar(14) NOT NULL,"
                      "  `apellido` varchar(16) NOT NULL,"
                      "  `genero` enum('M','F') NOT NULL,"
                      "  `fecha_contr` date NOT NULL,"
                      "  PRIMARY KEY (`n_empl`)"
                      ") ENGINE=InnoDB")

        try:
            cursor.execute(statement1)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                self.logger.error("La tabla ya existe")
            else:
                self.logger.error(err.msg)

    def execute_sql(self, sqlstring):
        """Ejecuta statements SQL"""

        self.logger.info("String SQL a ejecutar\n{}".format(sqlstring))
        cursor = self.cnx.cursor()
        try:
            cursor.execute(sqlstring)
        except RuntimeError:
            self.logger.error("Error de ejecucion de string SQL")
        else:
            cursor.close()
