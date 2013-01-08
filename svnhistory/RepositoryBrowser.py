# -*- coding: utf-8 -*-
# Copyright (C) 2012 Yunfei Zu <zuyunfei@gmail.com>

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.RepositoryBrowser import *
import pysvn
from time import *
from CodeHistoryViewer import CodeHistoryViewer
from MirrorServer import MirrorServerView, mirrorUrl


DataRole = Qt.UserRole + 1
ChildrenDataRow = Qt.UserRole + 2
iconProvider = QFileIconProvider()

def absoluteSvnPath(pysvnlist):
    return '%(path)s' % pysvnlist

def get_login( realm, username, may_save ):
    user = QInputDialog.getText(None, "Please Input User Name",
                                 "User Name")
    passwd = QInputDialog.getText(None, "Please Input Password",
                                  "Password", QLineEdit.Password)
    return user[1], str(user[0]), str(passwd[0]), True

svnClient = pysvn.Client()
svnClient.callback_get_login = get_login

def get_root_url(url):
    info = svnClient.info2(url, recurse=False)
    returner = ""
    try:
        returner = info[0][1]["repos_root_URL"]
    except Exception, e:
        print e
    return returner

class MirrorServersDialog(QDialog):
    def __init__(self, parent=None):
        super(MirrorServersDialog, self).__init__(parent)

class RepositoryDirModel(QStandardItemModel):
    def __init__(self, parent=None):
        super(RepositoryDirModel, self).__init__(parent)
        self.rootUrl = None

    def refresh(self, url):
        if not svnClient.is_url(url):
            print 'not valid url'
        self.clear()
        self.rootUrl = get_root_url(url)
        print self.rootUrl
        url = url[url.rfind(self.rootUrl) + len(self.rootUrl):]
        expandingTree = [self.rootUrl]
        for path in filter(None, url.split('/')):
            expandingTree.append('%s/%s' % (expandingTree[-1], path))
        print expandingTree
        self.addRootItem(expandingTree)

    def addRootItem(self, expandingTree=[]):
        self.rootRow = QStandardItem(self.rootUrl)
        pathlist = svnClient.list(self.rootUrl)
        self.rootRow.setData(pathlist[0], DataRole)
        self.appendRow(self.rootRow)
        self.addPathItems(self.rootUrl, self.rootRow, expandingTree)

    def addPathItems(self, path, parentRow, expandingTree=[]):
        pathInfoList = svnClient.list(path)
        parentRow.setData(pathInfoList, ChildrenDataRow)
        for pathInfo in pathInfoList:
            subPath = absoluteSvnPath(pathInfo[0])
            if subPath == path or pathInfo[0].kind != pysvn.node_kind.dir:
                continue
            childRow = QStandardItem(subPath[len(path):].strip('/'))
            childRow.setData(pathInfo, DataRole)
            parentRow.appendRow(childRow)
            if subPath in expandingTree:
                self.addPathItems(subPath, childRow, expandingTree)

    def expandPath(self, modelIndex, refresh=False):
        item = self.itemFromIndex(modelIndex)
        if item.hasChildren() and not refresh:
            return
        pathInfo = item.data(DataRole).toPyObject()
        path = absoluteSvnPath(pathInfo[0])
        self.addPathItems(path, item)

    # return QStandardItem
    def findPath(self, url):
        if url[-1] is '/': url = url[:-1]
        return self.findItem(url, self.rootRow)

    def findItem(self, url, parentRow):
        for i in range(parentRow.rowCount()):
            row = parentRow.child(i)
            data = row.data(DataRole).toPyObject()
            path = absoluteSvnPath(data[0])
            if path == url: return row
            item  = self.findItem(url, row)
            if item: return item
        return None


class RepositoryBrowser(QDialog, Ui_RepositoryBrowser):
    def __init__(self, cwd='', parent=None):
        super(RepositoryBrowser, self).__init__(parent)
        self.setupUi(self)
        self.urlComboBox.lineEdit().editingFinished.connect(self.on_urlEditingFinished)
        try:
            info = pysvn.Client().info(cwd)
            self.urlComboBox.setEditText(info.url)
        except pysvn.ClientError, e:
            print e
            self.urlComboBox.setEditText("")
        self.url = ""
        self.fileDetailTree.header().setResizeMode(QHeaderView.ResizeToContents)
        self.repositoryDirModel = RepositoryDirModel()
        self.repositoryTree.setModel(self.repositoryDirModel)

    def selectPath(self, url):
        item = self.repositoryDirModel.findPath(mirrorUrl(url))
        if not item: return
        self.selectPathItem(item)

    def selectPathItem(self, item):
        index = item.index()
        self.repositoryTree.selectionModel().clearSelection()
        self.repositoryTree.selectionModel().select(index, QItemSelectionModel.Select)
        parent = index
        while parent.isValid():
            self.repositoryTree.expand(parent)
            parent = parent.parent()
        self.repositoryTree.scrollTo(index, QAbstractItemView.PositionAtCenter)
        self.on_repositoryTree_clicked(index)

    def on_urlEditingFinished(self):
        url = str(self.urlComboBox.currentText())
        if self.url == url: return
        self.url = url
        self.repositoryDirModel.refresh(mirrorUrl(url))
        self.selectPath(url)

    def refreshFileDetailTree(self, pathInfoList):
        self.fileDetailTree.clear()
        if len(pathInfoList) < 2: return
        parentPath = absoluteSvnPath(pathInfoList[0][0])
        for pathInfo in pathInfoList[1:]:
            stringList = [absoluteSvnPath(pathInfo[0])[len(parentPath):].strip('/')]
            stringList.append(str(pathInfo[0].created_rev.number))
            stringList.append(pathInfo[0].last_author)
            stringList.append(strftime("%Y-%m-%d %H:%M:%S", gmtime(pathInfo[0].time)))
            item = QTreeWidgetItem(stringList)
            if pathInfo[0].kind == pysvn.node_kind.dir:
                item.setIcon(0, QIcon(iconProvider.icon(QFileIconProvider.Folder)))
            elif pathInfo[0].kind == pysvn.node_kind.file:
                item.setIcon(0, QIcon(iconProvider.icon(QFileIconProvider.File)))
            else:
                continue
            item.setData(0, DataRole, pathInfo)
            self.fileDetailTree.addTopLevelItem(item)

    def on_fileDetailTree_itemDoubleClicked(self, item):
        pathInfo = item.data(0, DataRole).toPyObject()
        if pathInfo[0].kind == pysvn.node_kind.file:
            return
        path = absoluteSvnPath(pathInfo[0])
        pathItem = self.repositoryDirModel.findPath(path)
        self.on_repositoryTree_clicked(pathItem.index())
        self.selectPathItem(pathItem)


    def on_repositoryTree_doubleClicked(self, modelIndex):
        self.on_repositoryTree_clicked(modelIndex)

    def on_repositoryTree_clicked(self, modelIndex):
        self.repositoryDirModel.expandPath(modelIndex)
        item = self.repositoryDirModel.itemFromIndex(modelIndex)
        childrenPathInfoList = item.data(ChildrenDataRow).toPyObject()
        self.refreshFileDetailTree(childrenPathInfoList)
        pathInfo = item.data(DataRole).toPyObject()
        path = absoluteSvnPath(pathInfo[0])
        self.urlComboBox.setEditText(path)
        self.url = path

    def on_viewHistoryBtn_pressed(self):
        url = str(self.urlComboBox.currentText())
        historyViewer = CodeHistoryViewer(self)
        historyViewer.refresh(mirrorUrl(url))
        historyViewer.exec_()

    def on_mirrorsBtn_pressed(self):
        dlg = MirrorServerView(self)
        dlg.exec_()
