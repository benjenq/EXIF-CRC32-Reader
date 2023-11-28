from PyQt5 import QtWidgets,QtGui,QtCore #PyQt5 的部分
from PyQt5.QtWidgets import *
import sys
import os
#https://improveandrepeat.com/2022/04/python-friday-120-modify-the-create-date-of-a-file/
#import filedate
from datetime import datetime
import math
import BeImageInfo
from BeLib.BeUtility import OSHelp
import UIExifGenDiag, BeLib.BeQtUI
import ErrDiag as Diag

class mainWin(QtWidgets.QDialog,UIExifGenDiag.Ui_Dialog):
    def __init__(self,parent=None,callback = None,rootPath:str = None):
        super(mainWin,self).__init__(parent)
        self.setupUi(self)
        if rootPath is None:
            self.rootPath.setText(OSHelp.launchPath())
        else:
            self.rootPath.setText(rootPath)
        self.progressBar.setValue(0)
        self.btnChooseDirectory.clicked.connect(self.openDirectoryDialog)
        self.btnWriteDB.clicked.connect(self.writeDB)
        BeLib.BeQtUI.doFixSize(self)
        BeLib.BeQtUI.toCenter(self)
        self.processing = False
        self.forceStop = False
        self.callBack = callback

    def openDirectoryDialog(self):
        dlg = QFileDialog()
        dlg.setDirectory(self.rootPath.text())
        chooseDirName = dlg.getExistingDirectory(self,"Select Directory")
        if(chooseDirName == ""):
            return
        self.rootPath.setText(os.path.normpath(chooseDirName)) #根據 OS 將目錄名稱正規化

    def setProgress(self,val):
        print("{:.02f}%".format(val))
        self.lb_progress.setText("{:.02f}%".format(val))
        self.progressBar.setValue(math.ceil(val))
        #https://stackoverflow.com/questions/30823863/pyqt-progress-bar-not-updating-or-appearing-until-100
        QtWidgets.QApplication.processEvents()

    def genFileTypes(self):
        fTypes = []
        if(self.chk_cr2.isChecked()):
            fTypes.append(".CR2") #用 extend 會拆成字元導致出錯。
        if(self.chk_cr3.isChecked()):
            fTypes.append(".CR3")
        if(self.chk_crw.isChecked()):
            fTypes.append(".CRW")
        if(self.chk_jpg.isChecked()):
            fTypes.append(".JPG")
            fTypes.append(".JPEG")
        if(self.chk_thm.isChecked()):
            fTypes.append(".THM")
        if(self.chk_mov.isChecked()):
            fTypes.append(".MOV")
        if len(fTypes) == 0:
            return ["*"]
        print(fTypes)
        return fTypes


    def writeDB(self):
        if self.processing:
            self.forceStop = True
            return
        files = OSHelp.genPathList(rootPath=self.rootPath.text(),extList=self.genFileTypes())
        ''' 改用 OSHelp.genPathList 所以棄用這個寫法
        for fType in self.genFileTypes():
            #aFiles = list(pathlib.Path(self.rootPath.text()).rglob(fType)) #rglob 不能用 rglob(*.JPG | *.CRW)
            aFiles = OSHelp.genPathList(self.rootPath.text())
            if len(aFiles) > 0:
                #files.append(aFiles) # 用append 會導致每個 item 都是 list 而不是檔案名稱會出錯
                files.extend(aFiles)
                #files = files + aFiles  #與 extend 同
        '''

        # 取得 fileinfo.txt 內容
        print("----- Start -----")
        self.btnWriteDB.setText("Cancel")
        totalFilesCnt = len(files)
        if totalFilesCnt == 0:
            print("------ Zero, End ------")
            self.setProgress(0)
            Diag.show(self,"No file found !")
            self.forceStop = False
            self.btnWriteDB.setText("Write to DB")
            return
        self.processing = True
        self.setCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        progress = 0
        self.setProgress(0)
        BeImageInfo.DBopen()
        BeImageInfo.DBBegin()
        doRollBack = False
        for f in files:
            if self.forceStop:
                doRollBack = True
                break
            # print(type(f))
            print(f.path)
            if os.path.isdir(f.path):
                # 顯示進度
                progress = progress +1
                val = 100*float(progress/totalFilesCnt)
                self.setProgress(val)
                continue
            if os.path.isfile(f.path):
                isSuccess = BeImageInfo.writeToDB(f.path,self.rootPath.text())
                if not isSuccess:
                    Diag.show(self,"writeToDB Error! ")
                    break
            # 顯示進度
            progress = progress +1
            val = 100*float(progress/totalFilesCnt)
            self.setProgress(val)
        self.processing = False
        self.forceStop = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        if doRollBack:
            BeImageInfo.DBRollback()
        else:
            BeImageInfo.DBCommit()
        BeImageInfo.DBclose()
        print("----- End -----")
        self.btnWriteDB.setText("Write to DB")
        if (progress/totalFilesCnt) >=1 :
            Diag.show(self,"Finish !!",False)

    def closeEvent(self, e: QtGui.QCloseEvent) -> None:
        if not (self.callBack is None):
            self.callBack(self.rootPath.text())
        return super().closeEvent(e)
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = mainWin()
    win.show()
    sys.exit(app.exec_())