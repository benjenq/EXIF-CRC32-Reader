from PyQt5 import QtWidgets,QtCore,QtGui #PyQt5 : pip3 install pyqt5
import UIErrDialog
from BeLib import BeUtility

class ErrorDialog(QtWidgets.QDialog, UIErrDialog.Ui_ErrDialog):
    def __init__(self,parent=None):
        super(ErrorDialog,self).__init__(parent)
        self.setupUi(self)
        self.btnOK.clicked.connect(self.closeSelf) #按下確定時
    def closeSelf(self):
        self.close()
    def closeEvent(self, evnt):
        pass
        #print("close Err")
        #evnt.ignore()

def show(parent:QtWidgets,text:str="",isErr = True):
    dlg = ErrorDialog(parent)
    if not isErr:
        dlg.setWindowTitle("Message")
        dlg.lb_errMsg.setStyleSheet("color : rgb(0 , 128 , 0)")
        dlg.setWindowIcon(BeUtility.icon("icon-info"))
        dlg.btnOK.setIcon(BeUtility.icon("icon-info"))
        dlg.btnOK.setStyleSheet("background-color : rgb(0 , 138 , 198);color : rgb(255 , 255 , 255)")
    dlg.lb_errMsg.setText(text) #主畫面的名字值
    dlg.exec_()
    dlg.destroy()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = ErrorDialog()
    win.show()
    sys.exit(app.exec_())