from PyQt5 import QtWidgets,QtCore,QtGui #PyQt5 : pip3 install pyqt5
from PyQt5.QtWidgets import *
import UIMain,ExifGen,ExifQuery,BeLib.BeQtUI

class mainWin(QtWidgets.QMainWindow,UIMain.Ui_Form):
    def __init__(self,parent=None):
        super(mainWin,self).__init__()
        self.setupUi(self)
        self.btnExifGen.clicked.connect(self.openExifWin)
        self.btnExifQuery.clicked.connect(self.openQueryWin)
        self.exifWin = None
        self.queryWin = None
        self.choosePath = None
        BeLib.BeQtUI.toCenter(self)
        BeLib.BeQtUI.doFixSize(self)
    
    def callBack(self,rootPath:str):
        self.choosePath = rootPath

    def openExifWin(self):
        if self.exifWin != None:
            self.exifWin.close()
            self.exifWin.destroy()
            self.exifWin = None
        if self.exifWin == None:
            self.exifWin = ExifGen.mainWin(parent=self, callback=self.callBack,rootPath=self.choosePath)
        self.exifWin.exec_()
        self.exifWin.close()
        self.exifWin.destroy()

    def openQueryWin(self):
        if self.queryWin != None:
            self.queryWin.close()
            self.queryWin.destroy()
            self.queryWin = None
        if self.queryWin == None:
            self.queryWin = ExifQuery.mainWin(parent=None,rootPath=self.choosePath)
        self.queryWin.show()
        self.queryWin.tb_Keyword.setFocus()
    
    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        choose = QtWidgets.QMessageBox.question(self,"Question","This App will close & exit.\nAre you sure?",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No )
        if choose == QtWidgets.QMessageBox.Yes:
            #return super().closeEvent(event)
            event.accept()
        else:
            event.ignore()

    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = mainWin()
    win.show()
    sys.exit(app.exec_())