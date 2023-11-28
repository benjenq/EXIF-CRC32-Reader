'''
取得 CRC32 / MD5 
---
'''
import zlib
import hashlib
import os


def getCRC32(fileName:str,checked:bool = True,compareCRC32:str=""):
    '''取得 CRC32
    ---
    fileName: 檔案路徑名稱\n
    checked : 是否檢核(False 則不做任何事回傳空字串)\n    
    compareCRC32 : 要對比的 CRC 值，回傳相符與否 True / False，空值則回傳 fileName 的 CRC 值
    '''
    if not checked:
        return ""
    if os.path.isdir(fileName):
        return ""
    with open(fileName, "rb") as f:
        byte = f.read()
    f.close()
    crc = str(hex(zlib.crc32(byte))[2:].upper())
    crc = "00000000{}".format(crc)[-8:]
    if(compareCRC32 == ""):
        return str(crc)
    else:
        if(str(crc) == compareCRC32):
            return True
        else:
            return False

def getMD5(fileName:str,checked:bool,compareMD5:str=""):
    '''取得 MD5
    ---
    fileName: 檔案路徑名稱\n
    checked : 是否檢核(False 則不做任何事回傳空字串)\n    
    compareMD5 : 要對比的 CRC 值，回傳相符與否 True / False，空值則回傳 fileName 的 CRC 值
    '''
    if not checked:
        return ""
    if os.path.isdir(fileName):
        return ""
    with open(fileName, "rb") as f:
        byte = f.read()
    f.close()
    m = hashlib.md5()
    m.update(byte)
    md5 = m.hexdigest()
    if(compareMD5 == ""):
        return str(md5.upper())
    else:
        if(str(md5).upper() == compareMD5):
            return True
        else:
            return False


    
    

    