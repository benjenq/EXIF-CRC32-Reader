# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'r:\EXIF_CRC32Reader\UIErrDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ErrDialog(object):
    def setupUi(self, ErrDialog):
        ErrDialog.setObjectName("ErrDialog")
        ErrDialog.setWindowModality(QtCore.Qt.WindowModal)
        ErrDialog.resize(298, 125)
        ErrDialog.setMinimumSize(QtCore.QSize(298, 125))
        ErrDialog.setMaximumSize(QtCore.QSize(298, 125))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/icon-error.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ErrDialog.setWindowIcon(icon)
        ErrDialog.setModal(True)
        self.btnOK = QtWidgets.QPushButton(ErrDialog)
        self.btnOK.setGeometry(QtCore.QRect(115, 85, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.btnOK.setFont(font)
        self.btnOK.setStyleSheet("background-color: rgb(185, 0, 0);\n"
"color: rgb(255, 255, 255);")
        self.btnOK.setIcon(icon)
        self.btnOK.setIconSize(QtCore.QSize(24, 24))
        self.btnOK.setObjectName("btnOK")
        self.lb_errMsg = QtWidgets.QLabel(ErrDialog)
        self.lb_errMsg.setGeometry(QtCore.QRect(10, 10, 281, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.lb_errMsg.setFont(font)
        self.lb_errMsg.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lb_errMsg.setStyleSheet("color: rgb(255, 0, 0);")
        self.lb_errMsg.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_errMsg.setWordWrap(True)
        self.lb_errMsg.setObjectName("lb_errMsg")

        self.retranslateUi(ErrDialog)
        QtCore.QMetaObject.connectSlotsByName(ErrDialog)

    def retranslateUi(self, ErrDialog):
        _translate = QtCore.QCoreApplication.translate
        ErrDialog.setWindowTitle(_translate("ErrDialog", "Error"))
        self.btnOK.setText(_translate("ErrDialog", "OK"))
        self.lb_errMsg.setText(_translate("ErrDialog", "This is a error message!"))
import resources_rc
