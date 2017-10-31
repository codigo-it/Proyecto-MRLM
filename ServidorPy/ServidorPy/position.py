import time

class positionClass:
    def __init__(self):
        self.bla=1
        #self.protocol = protocol
        #self.deviceid=deviceid
        #self.servertime=servertime
        #self.devicetime=devicetime
        #self.fixtime=fixtime
        #self.valid=valid
        #self.latitude=latitude
        #self.longitude=longitude
        #self.altitude=altitude
        #self.speed=speed
        #self.course=course
        #self.address=address
        #self.attributes=attributes
        #self.accuracy=accuracy
        #self.network=network

    def parseMessage(self,message):
        sp1=message.split("?")
        sp2=sp1[1].split(" ")
        sp3=sp2[0].split("&")
        for i in range(0,len(sp3)-1):
            aux=sp3[i].partition("=")
            sp3[i]=aux[2]

        self.protocol = 'osmand'
        self.deviceid = sp3[0]
        self.servertime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        self.devicetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(int(sp3[1])))
        self.fixtime = self.devicetime
        self.valid = '1'
        self.latitude = sp3[2]
        self.longitude = sp3[3]
        self.altitude = sp3[6]
        self.speed = sp3[4]
        self.course = sp3[5]
        self.address = 'Good question'
        self.attributes = 'Another good question'
        self.accuracy = sp3[7]

    def sqlPositionInsertion(self):
        string = "INSERT INTO `positions` (`id`, `protocol`, `deviceid`, `servertime`, `devicetime`, `fixtime`, `valid`, `latitude`, `longitude`, `altitude`, `speed`, `course`, `address`, `attributes`, `accuracy`, `network`) " \
        "VALUES (\" \", '{}', {}, '{}', '{}', '{}', {}, {}, {}, {}, {}, {}, '{}', '{}', {}, 'null')" \
        .format(self.protocol,self.deviceid,self.servertime,self.devicetime,self.fixtime,self.valid,self.latitude,self.longitude,self.altitude,self.speed,self.course,self.address,self.attributes,self.accuracy)
        return string


#Para pruebas de la clase
#pos1=position()
#pos1.parseMessage("b'POST /?id=327032&timestamp=1507767860&lat=-33.43413925876199&lon=-70.65783589013925&speed=2.1476642583031653&bearing=301.7934265136719&altitude=622.4467024936654&accuracy=301.7934265136719&batt=64.0 HTTP/1.1\r\nContent-Type: application/x-www-form-urlencoded\r\nUser-Agent: Dalvik/2.1.0 (Linux; U; Android 6.0.1; SM-G610M Build/MMB29K)\r\nHost: 192.168.1.30:10000\r\nConnection: Keep-Alive\r\nAccept-Encoding: gzip\r\nContent-Length: 0\r\n\r\n'")
#print(pos1.sqlPositionInsertion())



