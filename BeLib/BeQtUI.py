from PyQt5 import QtCore,QtGui,QtWidgets #PyQt5 的部分
from PyQt5.QtWidgets import *

class BeTableModel(QtCore.QAbstractTableModel):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self._data = data
        self._colTitle = []
        self.COLORS = ['#053061', '#2166ac', '#4393c3', '#92c5de', '#d1e5f0', '#f7f7f7', '#fddbc7', '#f4a582', '#d6604d', '#b2182b', '#67001f']
        if len(data) > 0:
            self._colTitle = list(data[0].keys())

    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if len(self._colTitle) > 0:
            titles = self._colTitle # should not be here for production code
        else:
            return None
        if role == QtCore.Qt.DisplayRole: # only change what DisplayRole returns
            if orientation == QtCore.Qt.Horizontal:
                return titles[section]
            elif orientation == QtCore.Qt.Vertical:
                return f'#{section + 1}'
        if role == QtCore.Qt.FontRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtGui.QFont('Arial',12)
        return super().headerData(section, orientation, role) # must have this line

    def colIndexToKey(self,col):
        if len(self._colTitle) > 0:
            return self._colTitle[col]

    def data(self, index, role):
        if not index.isValid():
            return None
        row = index.row()
        col = index.column()
        if role in {QtCore.Qt.DisplayRole}:
            #print("row={},col={},role={}".format(row,col,role))
            if isinstance(self._data[row][self.colIndexToKey(col)],int):
                #https://stackoverflow.com/questions/1823058/how-to-print-a-number-using-commas-as-thousands-separators
                return "{val:,}".format(val=self._data[row][self.colIndexToKey(col)])            
            return self._data[row][self.colIndexToKey(col)]
        if role in {QtCore.Qt.TextAlignmentRole}:
            if isinstance(self._data[row][self.colIndexToKey(col)],str) : 
                return  QtCore.Qt.AlignLeft
            else:
                return  QtCore.Qt.AlignTrailing #<class 'float'><class 'int'>

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
            self._data.sort(key=lambda item: item[self.colIndexToKey(column)],reverse=bool(order))
            self.layoutChanged.emit()
        except Exception as e:
            print(e)

def toCenter(ui:QtWidgets.QMainWindow):
    qr = ui.frameGeometry()
    cp = QDesktopWidget().availableGeometry().center()
    qr.moveCenter(cp)
    ui.move(qr.topLeft())

def doFixSize(ui:QtWidgets.QMainWindow):
    ui.setFixedSize(ui.frameGeometry().width(),ui.frameGeometry().height())


