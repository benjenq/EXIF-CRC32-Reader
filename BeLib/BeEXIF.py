import os,sys
#from PIL import Image # pip install Pillow #無法解 CRW
#import piexif # pip install piexif
#import exifread #無法解 CRW
#from rawkit.raw import Raw # Window 難安裝
#from exif import Image
if (sys.platform in ["win32","darwin","linux"]):
    import exiftool #pip3 install pyexiftool. macOS / Windows : 需要安裝 exiftool(/.exe) . linux : sudo apt install exiftool.
#import pyexiv2

def getMetaData(fileName:str) : # ->bool|dict: pyhon >= 3.10
    '''取得 EXIF 資訊
    ---
    fileName : 檔案名稱(含路徑)\n
    keyName: EXIF 的 Key 值
    '''
    if os.path.isdir(fileName):
        return False
    if not os.path.exists(fileName):
        return False
    try:
        with exiftool.ExifToolHelper(encoding="utf-8") as et: # 中文 Windows 預設 cp950 會出錯 
            metadata = et.get_metadata(files=fileName,params=["-charset","filename=utf-8"]) # 中文 Windows 指定編碼為 utf-8
            #print(metadata)
            #print("---------")
            #print(len(metadata))
            if len(metadata) == 0:
                return False            
            meta = metadata[0]
            dicExif = {}
            for key in meta:
                nKey = key.replace("MakerNotes:", "").replace("EXIF:", "").replace("Composite:","").replace("QuickTime:","")
                try:
                    val = dicExif[nKey]
                    if (val != meta[key]):
                        print("\"{}\"'s EXIF contains duplicate key [\"{}\"]: old value {}, new value {}".format(fileName,nKey,val,meta[key]))
                except Exception as e:
                    dicExif[nKey]=meta[key] 
                #print("{}\t\t{}".format(key, meta[key]))
            return dicExif
            #metadata.close()
            #basename = os.path.basename(fileName).split('.')[0] #不含副檔名
            #with open("{}.json".format(basename), 'w') as metadata:
                #metadata.write(json.dumps(items,indent=4))
                #metadata.close()
        
        '''
        md = pyexiv2.ImageMetadata(fileName)
        md.read()
        #print(md)
        
        # print all exif tags in file
        for key in md.exif_keys:
            try:
                if "EXIF.IMAGE.MODEL" in str(md[key]).upper():
                    print("{} :{}".format(key,str(md[key].value)))
                if "SERIAL" in str(md[key]).upper():
                    print("{} :{}".format(key,str(md[key].value)))
                if "FIRMWARE" in str(md[key]).upper():
                    print("{} :{}".format(key,str(md[key].value)))
                if "Exif.Canon.SerialNumber" == key:
                    #print(type(md[key].value))
                    if isinstance(md[key].value, int):
                        print(str(md[key].value))
                    else:
                        print(md[key].value[0])
            except Exception as e:
                print("{} Error: {}".format(type(e),str(e)))
                continue
        aperture = float(md['Exif.Photo.FNumber'].value)
        #print("Aperture: F{}".format(aperture))
        '''
    except Exception as e:
        print("***\"{}\" get EXIF err:{} - {}".format(fileName,type(e),str(e)))
        return False

    # <class 'PIL.Image.Exif'>
