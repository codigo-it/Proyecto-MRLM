"""Modulo que contiene la clase position
"""
import time


class Position:
    """Clase que guarda la info de posiciones recibidas"""

    # pylint: disable=too-many-instance-attributes
    # Se requieren 14 o mas

    def __init__(self):
        """Constructor
        """
        self.protocol = None
        self.deviceid = None
        self.servertime = None
        self.devicetime = None
        self.fixtime = None
        self.valid = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.speed = None
        self.course = None
        self.address = None
        self.attributes = None
        self.accuracy = None

    def parse_message_to_data(self, message):
        """Lee el mensaje del cliente trxxxar y guarda la info en el objeto 'position'"""

        #Primer parse para quitar informacion innecesaria de IP.
        sp1 = message.partition("?")
        if sp1[2] != '':
            #Segundo parse para quitar mensaje inutil.
            sp2 = sp1[2].partition(" ")
        else:
            print("Parse inicial malo")
            return 1

        #Tercer parse para obtener los pares 'nombre=atributo'.
        sp3 = sp2[0].split("&")

        if sp3[0] != '':
            for i in range(0, len(sp3)-1):
                #Cuarto parse que reutiliza sp3.
                aux = sp3[i].partition("=")
                sp3[i] = aux[2]
        else:
            print("Parse n3 malo")
            return 1

        #Quinto parse con revision de tipo correcto.
        try:
            self.protocol = 'osmand'
            self.deviceid = int(sp3[0])
            self.servertime = time.gmtime()
            self.devicetime = time.localtime(int(sp3[1]))
            self.fixtime = self.devicetime
            self.valid = '1'
            self.latitude = float(sp3[2])
            self.longitude = float(sp3[3])
            self.altitude = float(sp3[6])
            self.speed = float(sp3[4])
            self.course = float(sp3[5])
            self.address = 'Good question'
            self.attributes = 'Another good question'
            self.accuracy = float(sp3[7])
        except OSError:
            print("Excepcion en parse de atributos")
            return 1
        return 0

    def sql_position_insertion(self):
        """Genera la string sql para enviar al ejecutor
        """
        string = "INSERT INTO `positions` (`id`, `protocol`, `deviceid`, `servertime`, "\
                 "`devicetime`, `fixtime`, `valid`, `latitude`, `longitude`, `altitude`, "\
                 "`speed`, `course`, `address`, `attributes`, `accuracy`, `network`) "\
                 "VALUES (\" \", '{}', {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, '{}', "\
                 "'{}', {}, 'null')" \
        .format(self.protocol,\
        str(self.deviceid),\
        time.strftime("%Y-%m-%d %H:%M:%S", self.servertime),\
        time.strftime("%Y-%m-%d %H:%M:%S", self.devicetime),\
        time.strftime("%Y-%m-%d %H:%M:%S", self.fixtime),\
        self.valid,\
        str(self.latitude),\
        str(self.longitude),\
        str(self.altitude),\
        str(self.speed),\
        str(self.course),\
        self.address,\
        self.attributes,\
        str(self.accuracy))

        return string


#Para pruebas de la clase.
#pos1=position()
#pos1.parseMessage("b'POST /?id=327032&timestamp=1507767860&lat=-33.43413925876199&"\
#    "lon=-70.65783589013925&speed=2.1476642583031653&bearing=301.7934265136719&"\
#    "altitude=622.4467024936654&accuracy=301.7934265136719&batt=64.0 HTTP/1.1\r\n"\
#    "Content-Type: application/x-www-form-urlencoded\r\nUser-Agent: Dalvik/2.1.0 "\
#    "(Linux; U; Android 6.0.1; SM-G610M Build/MMB29K)\r\nHost: 192.168.1.30:10000\r\n"\
#    "Connection: Keep-Alive\r\nAccept-Encoding: gzip\r\nContent-Length: 0\r\n\r\n'")
#print(pos1.sqlPositionInsertion())
