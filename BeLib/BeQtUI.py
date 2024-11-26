from PyQt5 import QtCore,QtGui,QtWidgets #PyQt5 的部分
from PyQt5.QtWidgets import *

'''子模組互相 import, 問 chatGPT 得到的答案，回答有兩種寫法
其中 . 表示當前的目錄， .. 表示上一層目錄
from . import BeSQLDB
或
import sys
sys.path.append('..')
from BeLib import BeSQLDB
'''
from . import BeSQLDB

class BeTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self._colTitle = []
        self.BeColor = {'editColor':'#ffff99','previewColor' : '#e6f2ff','addrColor' : '#E2C8C9'}
        if len(data) > 0:
            self._colTitle = list(data[0].keys())

    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if len(self._colTitle) <= 0:
            return None
        if role == QtCore.Qt.DisplayRole: # only change what DisplayRole returns
            if orientation == QtCore.Qt.Horizontal:
                return self._colTitle[section]
            elif orientation == QtCore.Qt.Vertical:
                return f'#{section + 1}'
        if role == QtCore.Qt.FontRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtGui.QFont('Arial',12)
            if orientation == QtCore.Qt.Vertical:
                return QtGui.QFont('Arial',13)
        return super().headerData(section, orientation, role) # must have this line

    def colIndexToName(self,col):
        if len(self._colTitle) > 0:
            return self._colTitle[col]
        
    def colNameToIndex(self,colName:str):
        if len(self._colTitle) <= 0:
            return -1
        try:
            idx = self._colTitle.index(colName)
            return idx
        except Exception as e:
            return -1
    
    #QtCore.Qt.EditRole 可編輯 https://www.pythonguis.com/faq/editing-pyqt-tableview/
    def data(self, index, role):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if role in {QtCore.Qt.DisplayRole,QtCore.Qt.EditRole} :
            #print("row={},col={},role={}".format(row,col,role))
            if isinstance(self._data[row][self.colIndexToName(col)],int):
                #https://stackoverflow.com/questions/1823058/how-to-print-a-number-using-commas-as-thousands-separators
                return "{val:,}".format(val=self._data[row][self.colIndexToName(col)])            
            return self._data[row][self.colIndexToName(col)]
        if role in {QtCore.Qt.TextAlignmentRole}:
            if isinstance(self._data[row][self.colIndexToName(col)],str) : 
                return  QtCore.Qt.AlignLeft
            else:
                return  QtCore.Qt.AlignTrailing #<class 'float'><class 'int'>
        if role in {QtCore.Qt.BackgroundColorRole}:
            if self.colIndexToName(col) == "remark":
                return QtGui.QColor(self.BeColor["editColor"])
            if self.colIndexToName(col) == "relpath":
                return QtGui.QColor(self.BeColor["previewColor"])
            if self.colIndexToName(col) == "address":
                #找出 GPS 座標 gps_latitude, gps_longitude, gps_altitude
                if not (self._data[row]['gps_latitude'] == -1 and self._data[row]['gps_longitude'] == -1 and self._data[row]['gps_altitude'] == -1) :
                    return QtGui.QColor(self.BeColor["addrColor"])
        if role in {QtCore.Qt.ToolTipRole}:
            if self.colIndexToName(col) == "remark":
                return str("Double click to edit")
            if self.colIndexToName(col) == "relpath":
                return str("Double click to preview")
            if self.colIndexToName(col) == "address":
                if not (self._data[row]['gps_latitude'] == -1 and self._data[row]['gps_longitude'] == -1 and self._data[row]['gps_altitude'] == -1) :
                    return str("Double click to resolve address")
            

    
    #可編輯 https://www.pythonguis.com/faq/editing-pyqt-tableview/
    #編輯完Cell內容後觸發
    def setData(self, index:QtCore.QModelIndex, value, role):
        if role == QtCore.Qt.EditRole:
            if self.colIndexToName(index.column()) != "remark":
                return False
            # 從數字類型拖放到 remark 文字欄位，之後會出現以下錯誤，須將數字轉為文字
            # '<' not supported between instances of 'str' and 'float'
            oldValue = self._data[index.row()][self.colIndexToName(index.column())]
            nvalue = value
            if (not isinstance(value, str)) and isinstance(oldValue, str):
                nvalue = str(value)
            self._data[index.row()][self.colIndexToName(index.column())] = nvalue
            try:
                BeSQLDB.open()
                exifInfo = BeSQLDB.EXIFInfo(self._data[index.row()]["crc32"])
                exifInfo.remark = self._data[index.row()]["remark"]
                exifInfo.updateRemark()
                BeSQLDB.close()
            except Exception as e:
                print("{} Error : {}".format(type(e),str(e)))
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._data[0]) if self.rowCount() else 0

    #排序，設計工具中，QTableView 的 sortingEnabled 屬性要啟用，才會觸發此 sort 方法
    def sort(self, column, order):
        """Sort table by given column number. 排序
        https://stackoverflow.com/questions/28660287/sort-qtableview-in-pyqt5
        https://docs.python.org/zh-tw/3/howto/sorting.html
        """
        try:
            #print('column={},order={}'.format(column, order))
            self.layoutAboutToBeChanged.emit()            
            #self._data = sorted(self._data, key=lambda item: item[self.colIndexToKey(column)],reverse=bool(order))
            sortColumn = self.colIndexToName(column)
            if sortColumn == 'shutter':
                sortColumn = "shutterspeed"
            self._data.sort(key=lambda item: item[sortColumn],reverse=bool(order))
            self.layoutChanged.emit()
        except Exception as e:
            print(e)

    #可編輯 https://www.pythonguis.com/faq/editing-pyqt-tableview/
    def flags(self, index:QtCore.QModelIndex):
        colTitle = self._colTitle[index.column()]
        #僅 remark 欄位可編輯
        if colTitle == "remark":
            return QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsDragEnabled
        return QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsDragEnabled
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable

def toCenter(ui:QtWidgets.QMainWindow):
    qr = ui.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    ui.move(qr.topLeft())

def doFixSize(ui:QtWidgets.QMainWindow):
    ui.setFixedSize(ui.frameGeometry().width(),ui.frameGeometry().height())


