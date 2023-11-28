import sqlite3
dbFile = "ImgExif.db"
conn = None
noSelectedStr = "[Not Selected]"

def dict_factory(cursor, row):
    d:dict = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class EXIFInfo(object):
    global conn
    def __init__(self,crc32:str) -> None:
        self.crc32 = ""
        self.fileName = ""
        self.fileExt = ""
        self.relpath = ""
        self.orginalDateStr = ""
        self.orginalTimeStr = ""
        self.fileSize = -1

        self.aperture = -1
        self.shutterSpeed = -1
        self.iso = -1
        self.focalLength = -1
        self.minFocalLength = -1
        self.maxFocalLength = -1
        self.maxAperture = -1
        self.cameraMode = ""
        self.cameraSerial = ""
        self.lensMode = ""
        self.latitude = -1
        self.longitude = -1
        self.remark = ""
        l_sql = "SELECT crc32, filename, fileext, relpath, filesize, orginaldate, orginaltime, aperture, shutterspeed, iso, focallength, minfocallength, maxfocallength, maxaperture, cameramode, cameraserial, lensmode, \
                gps_latitude, gps_longitude, remark \
            FROM exifinfo WHERE crc32 = ? "
        try:
            conn.row_factory =  dict_factory #sqlite3.Row
            c = conn.execute(l_sql,(crc32,))
            for row in c:
                self.crc32 = row["crc32"]
                self.fileName = row["filename"]
                self.fileExt = row["fileext"]
                self.relpath = row["relpath"]
                self.fileSize = row["filesize"]
                self.orginalDateStr = row["orginaldate"]
                self.orginalTimeStr = row["orginaltime"]
                self.aperture = row["aperture"]
                self.shutterSpeed = row["shutterspeed"]
                self.iso = row["iso"]
                self.focalLength = row["focallength"]
                self.minFocalLength = row["minfocallength"]
                self.maxFocalLength = row["maxfocallength"]
                self.maxAperture = row["maxaperture"]
                self.cameraMode = row["cameramode"]
                self.cameraSerial = row["cameraserial"]
                self.lensMode = row["lensmode"]
                self.latitude = row["gps_latitude"]
                self.longitude = row["gps_longitude"]
                self.remark = row["remark"]

        except Exception as e:
            print("{} Error X : {}".format(type(e),str(e)))

    def updateDB(self):
        c = conn.cursor()
        try:
            l_sql = "INSERT OR REPLACE INTO exifinfo(\
            crc32,filename,fileext,relpath,filesize,orginaldate,orginaltime,aperture,shutterspeed,iso,focallength,minfocallength,maxfocallength,maxaperture,cameramode,cameraserial,lensmode,\
            gps_latitude, gps_longitude, remark \
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ;"
            c.execute(l_sql,(self.crc32,self.fileName,self.fileExt,self.relpath,self.fileSize,self.orginalDateStr,self.orginalTimeStr,self.aperture,self.shutterSpeed,self.iso,self.focalLength,self.minFocalLength,self.maxFocalLength,self.maxAperture,self.cameraMode,self.cameraSerial,self.lensMode,self.latitude,self.longitude,self.remark,))
            #l_sql = "INSERT OR REPLACE INTO exifinfo(crc32) VALUES(?);"
            #c.execute(l_sql,(self.crc32,))
            return True
        except Exception as e:
            print("{} Error : {}".format(type(e),str(e)))
            return False

    def delete(self):
        c = conn.cursor()
        c.execute("DELETE FROM exifinfo WHERE crc32 = ? ;",(self.crc32))

    def bindWithDic(self,exifDic:dict)->None:
        if(isinstance(exifDic,bool)):
            return
        self.aperture = round(float(self.readDict(exifDic,"FNumber","0")),1)
        self.minFocalLength = int(self.readDict(exifDic,"MinFocalLength","0"))
        self.maxFocalLength = int(self.readDict(exifDic,"MaxFocalLength","0"))
        self.maxAperture = round(float(self.readDict(exifDic,"MaxAperture","0")),1)
        self.shutterSpeed = float(self.readDict(exifDic,"ShutterSpeed","0"))
        self.orginalDateStr = str(self.readDict(exifDic,"DateTimeOriginal","x x")).split(" ")[0].replace(":", "-")
        self.orginalTimeStr = str(self.readDict(exifDic,"DateTimeOriginal","x x")).split(" ")[1]
        self.iso = int(self.readDict(exifDic,"ISO","0"))
        self.focalLength = int(self.readDict(exifDic,"FocalLength","0"))
        self.cameraMode = str(self.readDict(exifDic,"Model"))
        self.cameraSerial = str(self.readDict(exifDic,"SerialNumber"))
        self.lensMode = str(self.readDict(exifDic,"LensModel"))
        if(self.lensMode == ""):
            if (self.minFocalLength != self.maxFocalLength):
                self.lensMode = "EF{}-{}mm f/{}".format(self.minFocalLength,self.maxFocalLength,self.maxAperture)
            else:
                self.lensMode = "EF{}mm f/{}".format(self.minFocalLength,self.maxAperture)
    
    def readDict(self,exDict:dict,key:str,nullval:str=None):
        if nullval == None:
            nullval = ""
        try:
            result = exDict[key]
            if result=="undef":
                result = nullval
            return result
        except Exception as e:
            print("{} : {}".format(type(e),str(e)))
            return nullval
        #print(exifDic)

def getCameraList():
    result = getCBItemsList("SELECT DISTINCT cameramode as cameramode FROM exifinfo ORDER BY cameramode ;","cameramode")
    return result
def getLensList():
    result = getCBItemsList("SELECT DISTINCT lensmode as lensmode FROM exifinfo ORDER BY lensmode ;","lensmode")
    return result

def queryResult(cameramode:str,lensmode:str,keyword:str = ""):
    global conn
    l_sql = "SELECT * FROM exifinfo WHERE 1=1 "
    if cameramode != noSelectedStr:
        l_sql = l_sql + " AND cameramode = '{}' ".format(cameramode)
    if lensmode != noSelectedStr:
        l_sql = l_sql + " AND lensmode = '{}' ".format(lensmode)
    if keyword != "":
        l_sql = l_sql + " AND (relpath LIKE '%{keyword}%' OR orginaldate LIKE '%{keyword}%' ) ".format(keyword=keyword)    
    l_sql = l_sql + " LIMIT 500; "
    open()
    conn.row_factory = dict_factory #sqlite3.Row
    rows = conn.execute(l_sql).fetchall()
    close()
    return rows
    result = []
    for row in rows:
        item = EXIFInfo(row["crc32"])
        result.append(item)
    close()
    return result

def getCBItemsList(l_sql:str,field:str):
    '''產生 ComboBox 元素
    ---
    l_sql : SQL 語法\n
    field : 元素名
    '''
    global conn
    open()
    conn.row_factory =  dict_factory #sqlite3.Row
    c = conn.execute(l_sql)
    result = [noSelectedStr]
    for row in c:
        result.append(row[field])
    close()
    return result

def BEGIN():
    global conn
    conn.isolation_level = None
    c = conn.cursor()
    c.execute("BEGIN")

def COMMIT():
    global conn
    c = conn.cursor()
    c.execute("COMMIT")

def ROLLBACK():
    global conn
    c = conn.cursor()
    c.execute("ROLLBACK")

def open():
    global conn
    conn = sqlite3.connect(database=dbFile)

def close():
    global conn
    conn.commit()
    conn.close()
    conn == None