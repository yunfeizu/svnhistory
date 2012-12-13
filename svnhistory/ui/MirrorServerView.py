# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MirrorServerView.ui'
#
# Created: Fri Dec 14 01:18:01 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MirrorServerView(object):
    def setupUi(self, MirrorServerView):
        MirrorServerView.setObjectName(_fromUtf8("MirrorServerView"))
        MirrorServerView.resize(400, 245)
        self.verticalLayout = QtGui.QVBoxLayout(MirrorServerView)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.serverTableWidget = QtGui.QTableWidget(MirrorServerView)
        self.serverTableWidget.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.serverTableWidget.setShowGrid(True)
        self.serverTableWidget.setObjectName(_fromUtf8("serverTableWidget"))
        self.serverTableWidget.setColumnCount(3)
        self.serverTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.serverTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.serverTableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.serverTableWidget.setHorizontalHeaderItem(2, item)
        self.serverTableWidget.horizontalHeader().setStretchLastSection(True)
        self.serverTableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.serverTableWidget)
        self.buttonBox = QtGui.QDialogButtonBox(MirrorServerView)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(MirrorServerView)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MirrorServerView.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MirrorServerView.reject)
        QtCore.QMetaObject.connectSlotsByName(MirrorServerView)

    def retranslateUi(self, MirrorServerView):
        MirrorServerView.setWindowTitle(QtGui.QApplication.translate("MirrorServerView", "Mirror Servser", None, QtGui.QApplication.UnicodeUTF8))
        item = self.serverTableWidget.horizontalHeaderItem(1)
        item.setText(QtGui.QApplication.translate("MirrorServerView", "Server", None, QtGui.QApplication.UnicodeUTF8))
        item = self.serverTableWidget.horizontalHeaderItem(2)
        item.setText(QtGui.QApplication.translate("MirrorServerView", "Mirror", None, QtGui.QApplication.UnicodeUTF8))

