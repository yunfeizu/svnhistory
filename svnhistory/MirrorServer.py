# -*- coding: utf-8 -*-
# Copyright (C) 2012 Yunfei Zu <zuyunfei@gmail.com>

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.MirrorServerView import *

mirrorServers = [(True, "svn.sr.elekta.se" , "mirror.elekta.shanghai/svn")]


def mirrorUrl(url):
    for enabled, server, mirror in mirrorServers:
        if server in url and enabled:
            return url.replace(server, mirror)
    return url

class MirrorServerView(QDialog, Ui_MirrorServerView):
    def __init__(self, parent=None):
        super(MirrorServerView, self).__init__(parent)
        self.setupUi(self)
        self.serverTableWidget.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.loadServers()

    def loadServers(self):
        self.serverTableWidget.clearContents()
        self.serverTableWidget.setRowCount(len(mirrorServers))
        for row, server in zip(range(len(mirrorServers)), mirrorServers):
            checkItem = QTableWidgetItem()
            checkItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            checkItem.setCheckState(Qt.Checked if server[0] else Qt.Unchecked)
            checkItem.setTextAlignment(Qt.AlignHCenter)
            self.serverTableWidget.setItem(row, 0, checkItem)
            self.serverTableWidget.setItem(row, 1, QTableWidgetItem(server[1]))
            self.serverTableWidget.setItem(row, 2, QTableWidgetItem(server[2]))

    def mirrorServers(self):
        servers = []
        for i in range(self.serverTableWidget.rowCount()):
            enabled = self.serverTableWidget.item(i, 0).checkState() == Qt.Checked
            server = str(self.serverTableWidget.item(i, 1).text())
            mirror = str(self.serverTableWidget.item(i, 2).text())
            servers.append((enabled, server, mirror))
        return servers

    def accept(self):
        global mirrorServers
        mirrorServers = self.mirrorServers()
        super(MirrorServerView, self).accept()
