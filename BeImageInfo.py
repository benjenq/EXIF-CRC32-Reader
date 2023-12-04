import os
from BeLib import BeHash,BeEXIF , BeSQLDB

def writeToDB(imgFileName:str,rootPath="") -> bool:
    '''將圖檔資訊(含EXIF)寫入資料庫
    ---
    imgFileName : 圖檔檔名與路徑\n
    rootPath  : 根路徑，用來取得相對路徑
    '''
    if os.path.isdir(imgFileName):
        return False
    crc32 = BeHash.getCRC32(imgFileName,True)
    dbExif = BeSQLDB.EXIFInfo(crc32)
    dbExif.crc32 = crc32
    dbExif.fileName = os.path.basename(imgFileName).split(".")[0]
    dbExif.fileExt = os.path.basename(imgFileName).split(".")[1].upper() #副檔名大寫
    relPath = os.path.relpath(imgFileName,rootPath)
    dbExif.relpath = relPath
    dbExif.fileSize = int(os.stat(imgFileName).st_size)
    exifInfo = BeEXIF.getMetaData(imgFileName)
    if not exifInfo:
        return False
    dbExif.bindWithDic(exifInfo)
    return dbExif.updateDB()

def DBopen():
    BeSQLDB.open()

def DBclose():
    BeSQLDB.close()

def DBBegin():
    BeSQLDB.BEGIN()

def DBCommit():
    BeSQLDB.COMMIT()

def DBRollback():
    BeSQLDB.ROLLBACK()


