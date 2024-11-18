
from PyQt5 import QtWidgets,QtGui
import os,sys,pathlib


iconSet={"icon-image" : ":/icon/icon/icon-image.png",
         "icon-edit" :":/icon/icon/icon-edit.png",
         "icon-done" : ":/icon/icon/icon-done.png",
         "icon-info" : ":/icon/icon/icon-info.png",
         "icon-gps" : ":/icon/icon/icon-gps.png"}

def toClipBoard(string:str):
    cb = QtWidgets.QApplication.clipboard()
    cb.clear(mode=cb.Clipboard )
    cb.setText(str(string), mode=cb.Clipboard)

def icon(iconName:str):
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(iconSet[iconName]), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    return icon

class OSHelp(object):
    @staticmethod
    def launchPath():
        '''
        起始目錄
        '''
        if(sys.platform == "darwin"):
            dirPath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(sys.argv[0]))))
        else:
            #dirPath = os.path.dirname(os.path.abspath(__file__)) #os.path.dirname(sys.argv[0])
            dirPath = os.path.abspath(os.path.curdir)
        #TODO: pyinstaller 時標記下面這行
        #dirPath = os.path.dirname(path.abspath(__file__)) #pyinstaller
        return dirPath

    @staticmethod
    def genPathList(rootPath:str,extList:list = None, lst:list = None) ->list:
        '''產生檔案與目錄集
        ---
        rootPath: 根目錄\n
        extList: 副檔名 LIst, 如 ['.JPEG','.CR2'],  ['*'] 為包含目錄 
        lst : <class 'nt.DirEntry'> 物件的 List 集合
        '''
        if extList == None:
            extList = ["*"]
        if lst == None:
            lst = []
        try:
            for f in os.scandir(rootPath):
                #print(type(f))
                if f.is_dir():
                    if extList == ['*']:
                        lst.append(f)
                    OSHelp.genPathList(f.path,extList,lst)
                elif f.is_file():
                    if pathlib.Path(f.path).suffix.upper() in extList or extList == ['*']:
                        lst.append(f)
        except Exception as e:
            print("\"{}\" {}:{}".format(rootPath, type(e),str(e)))
        return lst
