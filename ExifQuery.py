from PyQt5 import QtWidgets,QtCore,QtGui #PyQt5 的部分
from PyQt5.QtWidgets import *
import UIQuery,ErrDiag
import os,sys,webbrowser #ImagePreview
from BeLib import BeSQLDB,BeUtility,BeGPS
from BeLib.BeUtility import OSHelp
import BeLib.BeQtUI
from BeLib.BeQtUI import BeTableModel
if (sys.platform in ["darwin","linux"]):
    import subprocess

#Table View 用法： https://zhung.com.tw/article/table-data-model-and-view-in-qt-for-python/
# https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/


class mainWin(QtWidgets.QMainWindow,UIQuery.Ui_MainWindow):
    def __init__(self, parent=None, rootPath:str=None):
        super(mainWin,self).__init__(parent)
        self.setupUi(self)
        self.genCBItems(self.cb_camera, BeSQLDB.getCameraList())
        self.genCBItems(self.cb_lens, BeSQLDB.getLensList())
        self.btnQuery.clicked.connect(self.doQuery)
        if rootPath is None:
            self.rootPath.setText(OSHelp.launchPath())
        else:
            self.rootPath.setText(rootPath)
        self.btnChooseDirectory.clicked.connect(self.openDirectoryDialog)
        self.tbv_data.doubleClicked.connect(self.tableViewDblClicked)

        #https://stackoverflow.com/questions/28186118/how-to-make-qtableview-to-enter-the-editing-mode-only-on-double-click
        #停用 鍵盤觸發編輯模式 (預設值會觸發，當 remark 欄隨意按下任一鍵盤字母就觸發)
        self.tbv_data.setEditTriggers(QAbstractItemView.NoEditTriggers |
                             QAbstractItemView.DoubleClicked)
        #設定欄位內容可用滑鼠拖放
        self.tbv_data.setDragDropMode(QAbstractItemView.DragDrop)
        BeLib.BeQtUI.toCenter(self)
        #關鍵字監聽事件
        self.tb_Keyword.installEventFilter(self) #對應 def eventFilter(self, source, event):
        #self.tb_Keyword.textEdited.connect(self.showCurrentText)
        #self.tb_Keyword.keyPressEvent = self.keyWordPressEvent 
    ''' 每輸入一字元都會觸發，但輸入 Enter/Return 不會觸發
    def showCurrentText(self, text):
        print('current-text:', text) #'''

    ''' 文字欄位會攔截輸入文字導致不顯示在文字欄位上，所以停用
    def keyWordPressEvent(self, e: QtGui.QKeyEvent) :
        print(str(e))
        if e.key() == QtCore.Qt.Key_Return:
            self.doQuery()
        else:
            return super(type(mainWin), self).keyPressEvent(e) #'''
    
    ''' 表示整個 WindowForm 的 KeyPress 事件
    def keyPressEvent(self, a0: QtGui.QKeyEvent) 
        return super().keyPressEvent(a0)  #'''
    
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and source is self.tb_Keyword):
            #print('key press:', (event.key(), event.text()))
            if(event.key() == QtCore.Qt.Key_Return):
                self.doQuery()
        return super(mainWin, self).eventFilter(source, event) #https://stackoverflow.com/questions/50768366/installeventfilter-in-pyqt5
    
    def genCBItems(self, obj, items:list): #產生下拉項目
        for item in items:
            obj.addItem(item)

    def doQuery(self):
        success, ds = BeSQLDB.queryResult(self.cb_camera.currentText(),self.cb_lens.currentText(),self.tb_Keyword.text())
        if not success:
            ErrDiag.show(self,str(ds),True)
            return
        self.model = BeTableModel(ds)
        self.tbv_data.setModel(self.model)
        self.tbv_data.hideColumn(self.model.colNameToIndex('crc32'))
        self.tbv_data.hideColumn(self.model.colNameToIndex('shutterspeed'))
        self.tbv_data.hideColumn(self.model.colNameToIndex('gps_latitude'))
        self.tbv_data.hideColumn(self.model.colNameToIndex('gps_longitude'))
        self.tbv_data.hideColumn(self.model.colNameToIndex('gps_altitude'))
        if(len(ds) >0): #有資料
            #https://stackoverflow.com/questions/38098763/pyside-pyqt-how-to-make-set-qtablewidget-column-width-as-proportion-of-the-a
            header = self.tbv_data.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.ResizeToContents)
            if(len(ds)>1):
                self.tbv_data.sortByColumn(0,QtCore.Qt.SortOrder.AscendingOrder)

    def tableViewDblClicked(self, clickedEvent:QtCore.QModelIndex):
        clickedField = clickedEvent.model()._colTitle[clickedEvent.column()]
        clickedData = clickedEvent.data()
        if clickedField != "remark":
            BeUtility.toClipBoard(clickedData)
        if clickedField == "relpath":
            self.previewImage(clickedData)
        if clickedField == "address":
            clickedItem = self.tbv_data.model()._data[clickedEvent.row()]
            if not (clickedItem['gps_latitude'] == -1 and clickedItem['gps_longitude'] == -1 and clickedItem['gps_altitude'] == -1):
                self.ReverseAddr(clickedItem['crc32'],clickedItem['gps_latitude'],clickedItem['gps_longitude'])

    #https://stackoverflow.com/questions/60922666/create-different-context-menus-on-several-qtableviews
    #右鍵選單
    def contextMenuEvent(self, event:QtGui.QContextMenuEvent):
        if self.tbv_data.underMouse(): #點擊到 TableView 物件            
            selectedModel = self.tbv_data.selectionModel()
            if selectedModel is None: #TableView 內沒有 Model，意即沒有資料
                return
            selected_data = None #Cell 內的文字內容
            column = None #點擊了第幾個欄位對應的 Key 值
            for index in selectedModel.selectedIndexes():
                selected_data = index.data() #Cell 內的文字內容
                column = index.model()._colTitle[index.column()] #relpath
            #if selected_data is None:
            #    return
            contextMenu = QMenu(self)
            copyAct = contextMenu.addAction(BeUtility.icon("icon-done"), "&Copy")
            previewAct = None
            editAct = None
            gpsAct = None
            gpsReverse = None
            if column == "relpath": #點擊了路徑欄位
                previewAct = contextMenu.addAction(BeUtility.icon("icon-image"), "&Preview")
            if column == "remark": #點擊了路徑欄位
                editAct = contextMenu.addAction(BeUtility.icon("icon-edit"), "&Edit")
            if column in ['gps_latitude', 'gps_longitude', 'gps_altitude','address']:
                select_item = selectedModel.model()._data[self.tbv_data.currentIndex().row()]
                if not (select_item['gps_latitude'] == -1 and select_item['gps_longitude'] == -1 and select_item['gps_altitude'] == -1):
                    if column in ['gps_latitude', 'gps_longitude', 'gps_altitude']:
                        gpsAct = contextMenu.addAction(BeUtility.icon("icon-gps"), "&Google Map")
                    elif column in ['address']:
                        gpsAct = contextMenu.addAction(BeUtility.icon("icon-gps"), "&Google Map")
                        gpsReverse = contextMenu.addAction(BeUtility.icon("icon-reverse"), "&GPS Reverse")
            action = contextMenu.exec_(self.mapToGlobal(event.pos()))
            if action is None: #點擊到選單以外的部分
                return
            if action == copyAct and selected_data != None:
                BeUtility.toClipBoard(selected_data)
                return
            if action == previewAct and selected_data != None:
                self.previewImage(selected_data)
                return
            if action == editAct:
                self.tbv_data.edit(self.tbv_data.currentIndex())
                return
            if action == gpsAct:
                if select_item == None:
                    return
                urlstr = f'http://maps.google.com/?q={select_item['gps_latitude']},{select_item['gps_longitude']}'
                webbrowser.open(urlstr)
                return
            if action == gpsReverse:
                if select_item == None:
                    return
                self.ReverseAddr(select_item['crc32'], select_item['gps_latitude'], select_item['gps_longitude'])
                return
    
    def ReverseAddr(self,crc32:str,latitude:float,longitude:float):
        success, addr = BeGPS.Reverse(latitude,longitude)
        if not success:
            ErrDiag.show(self,addr,True)
            return
        ds =  self.tbv_data.model()._data
        for item in ds:
            if item['crc32'] == crc32:
                item['address'] = f'{addr}'
                BeSQLDB.open()
                exifInfo = BeSQLDB.EXIFInfo(crc32)
                exifInfo.address = addr
                exifInfo.updateAddr()
                BeSQLDB.close()
        # https://stackoverflow.com/questions/27592088/how-to-refresh-qtableview-when-it-is-driven-by-model
        self.tbv_data.viewport().update()

    def previewImage(self, imgPath:str):
        '''系統預設開啟檔案
        ---
        imgPath: 檔案相對路徑
        '''
        if imgPath is None:
            ErrDiag.show(self,"File \"{}\" not Found!".format("None"),True)
            return
        sPath = os.path.join(self.rootPath.text(),imgPath)
        if not os.path.exists(sPath):
            if sys.platform == "win32":
                sPath = sPath.replace("/","\\")
            else: #macOS = darwin, Linux = linux
                sPath = sPath.replace("\\","/")
            if not os.path.exists(sPath):
                ErrDiag.show(self, "File \"{}\" not Found!".format(sPath), True)
                return
        BeUtility.toClipBoard(sPath)
        if (sys.platform in ["win32"]):
            os.startfile(sPath)
        else:
            subprocess.call(["open", sPath])

    def openDirectoryDialog(self):
        dlg = QFileDialog()
        dlg.setDirectory(self.rootPath.text())
        chooseDirName = dlg.getExistingDirectory(self, "Select Directory")
        if(chooseDirName == ""):
            return
        self.rootPath.setText(os.path.normpath(chooseDirName)) #根據 OS 將目錄名稱正規化

    def closeEvent(self, event:QtGui.QCloseEvent) -> None:
        event.accept()
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = mainWin()
    win.show()
    win.tb_Keyword.setFocus()
    sys.exit(app.exec_())