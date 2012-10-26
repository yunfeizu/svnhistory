# -*- coding: utf-8 -*-
# Copyright (C) 2012 Yunfei Zu <zuyunfei@gmail.com>

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from ui.CodeHistoryViewer import *
import os
import pysvn
from time import strftime, gmtime

class CodeCommit():
    def __init__(self, svnLog):
       self.revision = svnLog["revision"]
       self.author = svnLog["author"]
       self.message = svnLog["message"]
       self.date = svnLog["date"]
       self.changedPaths = svnLog["changed_paths"]

    def revisionInfo(self):
        return [str(self.revision.number), self.author, strftime("%Y-%m-%d %H:%M:%S", \
                gmtime(self.date))]

    def changedPathsInfo(self):
        return [[path["action"], path["path"], ('' if path["copyfrom_path"] is None else \
                path["copyfrom_path"])] for path in self.changedPaths]


class CodeHistoryModel(QAbstractTableModel):
    def __init__(self, parent = None):
        super(CodeHistoryModel, self).__init__(parent)
        self.headers = {0:"Revision", 1:"Author", 2:"Date"}
        self.commits = []

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole and self.headers.has_key(section):
                return self.headers[section]
            return QVariant()
        return super(CodeHistoryModel, self).headerData(section, orientation, role)

    def rowCount(self, parent=QModelIndex()):
        return len(self.commits)

    def columnCount(self, parent=QModelIndex()):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if (index.row() < 0 and index.row() >= len(self.commits)):
            return QVariant()
        if role == Qt.DisplayRole:
            return self.commits[index.row()].revisionInfo()[index.column()]
        elif role == Qt.UserRole:
            return self.commits[index.row()]
        return QVariant()


    def refresh(self, url):
        svnClient = pysvn.Client()
        logs = svnClient.log(url_or_path = url, discover_changed_paths = True)
        self.commits = [CodeCommit(log) for log in logs]
        self.reset

def keywordHighlightHtml(string, keyword, color):
    return string.replace(keyword, '<span style="background-color:%s">%s</span>' \
            % (color, keyword)) if len(keyword) > 0 else string

def anyKeywordsInStringList(keywords, stringList):
    if not keywords: return True
    for keyword in keywords:
        for string in stringList:
            if keyword in string:
                return True
    return False

class CodeHistoryFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(CodeHistoryFilterProxyModel, self).__init__(parent)
        self.author = ''
        self.reviewers = []
        self.from_date = ''
        self.to_date = ''
        self.from_revision = 0
        self.to_revision = 0
        self.pathKeywords= []
        self.logKeywords = []

    def setFilter(self, author='', reviewers=[], pathKeywords='', logKeywords=[], from_date='', \
            to_date='', from_revision='', to_revision=''):
        self.author = author
        self.reviewers = ['<%s>' % reviewer if reviewer else '' for reviewer in reviewers]
        self.pathKeywords = pathKeywords
        self.logKeywords = logKeywords
        self.reset()

    def filterAcceptsRow(self, sourceRow, sourceParent):
        sourceModel = self.sourceModel()
        indexColumn0 = sourceModel.index(sourceRow, 0, sourceParent)
        indexColumn1 = sourceModel.index(sourceRow, 1, sourceParent)
        indexColumn2 = sourceModel.index(sourceRow, 2, sourceParent)
        commit = indexColumn1.data(Qt.UserRole).toPyObject()
        if self.author not in sourceModel.data(indexColumn1):
            return False
        if not anyKeywordsInStringList(self.reviewers, [commit.message]):
            return False
        if not anyKeywordsInStringList(self.pathKeywords,
                [pathInfo[1] for pathInfo in commit.changedPathsInfo()]):
            return False
        if not anyKeywordsInStringList(self.logKeywords, [commit.message]):
            return False
        return True

    def data(self, index, role=Qt.DisplayRole):
        sourceIndex = self.mapToSource(index)
        if not sourceIndex.isValid():
            return QVariant()
        if role == Qt.DisplayRole:
            if sourceIndex.column() == 1 and self.author:
                return keywordHighlightHtml(sourceIndex.data(role).toString(), self.author, "deepskyblue")
        return sourceIndex.data(role)

class ChangedFileModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(ChangedFileModel, self).__init__(parent)
        self.headers = {0:"Action", 1:"Path", 2:"Copy from path"}
        self.workingPath = ''
        self.changeFiles = []
        self.pathKeywords = []

    def rowCount(self, parent=QModelIndex()):
        return len(self.changeFiles)

    def columnCount(self, parent=QModelIndex()):
        return 3

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()
        if (index.row() < 0 and index.row() >= len(self.changeFiles)):
            return QVariant()
        if role == Qt.DisplayRole:
            data = self.changeFiles[index.row()][index.column()]
            if index.column() == 1:
                data = data[data.find(self.workingPath) + len(self.workingPath):]
                for pathKeyword in self.pathKeywords:
                    data = keywordHighlightHtml(data, pathKeyword, "red")
            return data

        elif role == Qt.UserRole:
            return self.changeFiles[index.row()][1]
        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole and self.headers.has_key(section):
                return self.headers[section]
            return QVariant()
        return super(CodeHistoryModel, self).headerData(section, orientation, role)


    def refresh(self, changedFiles, workingPath, pathKeywords):
        self.changeFiles = changedFiles
        self.pathKeywords = pathKeywords
        self.reset()

class HTMLDelegate(QtGui.QStyledItemDelegate):
    def paint(self, painter, option, index):
        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options,index)

        style = QtGui.QApplication.style() if options.widget is None else options.widget.style()

        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)

        options.text = ""
        style.drawControl(QtGui.QStyle.CE_ItemViewItem, options, painter);

        ctx = QtGui.QAbstractTextDocumentLayout.PaintContext()

        # Highlighting text if item is selected
        #if (optionV4.state & QStyle::State_Selected)
            #ctx.palette.setColor(QPalette::Text, optionV4.palette.color(QPalette::Active, QPalette::HighlightedText));

        textRect = style.subElementRect(QtGui.QStyle.SE_ItemViewItemText, options)
        painter.save()
        painter.translate(textRect.topLeft())
        painter.setClipRect(textRect.translated(-textRect.topLeft()))
        doc.documentLayout().draw(painter, ctx)

        painter.restore()

    def sizeHint(self, option, index):
        options = QtGui.QStyleOptionViewItemV4(option)
        self.initStyleOption(options,index)

        doc = QtGui.QTextDocument()
        doc.setHtml(options.text)
        doc.setTextWidth(options.rect.width())
        return QtCore.QSize(doc.idealWidth(), doc.size().height())

class SyntaxHighlighter(QSyntaxHighlighter):

    class HighlightingRule():
        def __init__(self, pattern, format):
            self.pattern = pattern
            self.format = format

    def __init__(self, parent=None):
        super(SyntaxHighlighter, self).__init__(parent)
        self.highlightingRules = []

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = text.indexOf(expression, index + length)
        self.setCurrentBlockState(0)

class LogSyntaxHighlighter(SyntaxHighlighter):
    def __init__(self, parent=None):
        super(LogSyntaxHighlighter, self).__init__(parent)
        self.keywordsRules = []
        self.basicRules = []
        self.reviewerRules = []

        #highlight reviewer in message <...>
        reviewerFormat = QTextCharFormat();
        reviewerFormat.setFontWeight(QFont.Black)
        # reviewerFormat.setForeground(Qt.green)
        reviewerExp = QRegExp("<\S[^>]+>")
        self.basicRules.append(SyntaxHighlighter.HighlightingRule(reviewerExp, reviewerFormat))

        #highlight workpackage or project in message [...]
        wpFormat = QTextCharFormat();
        wpFormat.setFontWeight(QFont.Black)
        wpExp = QRegExp("\[\S[^>]+\]")
        self.basicRules.append(SyntaxHighlighter.HighlightingRule(wpExp, wpFormat))

        #highlight PR (TPS-...)
        prFormat = QTextCharFormat();
        prFormat.setFontWeight(QFont.Black)
        prExp = QRegExp("TPS-\d+", Qt.CaseInsensitive)
        self.basicRules.append(SyntaxHighlighter.HighlightingRule(prExp, prFormat))

        #highlight Task (CONN-...)
        taskFormat = QTextCharFormat();
        taskFormat.setFontWeight(QFont.Black)
        taskExp = QRegExp("CONN-\d+", Qt.CaseInsensitive)
        self.basicRules.append(SyntaxHighlighter.HighlightingRule(taskExp, taskFormat))


    def highlightKeywords(self, keywords):
        keywordFormat = QTextCharFormat()
        keywordFormat.setBackground(Qt.yellow)
        keywordFormat.setFontWeight(QFont.Black)
        self.keywordsRules = []
        for keyword in keywords:
            pattern = QRegExp("\\b%s\\b" % keyword)
            rule = SyntaxHighlighter.HighlightingRule(pattern, keywordFormat)
            self.keywordsRules.append(rule)

    def highlightReviewers(self, reviewers):
        reviewerFormat = QTextCharFormat()
        reviewerFormat.setBackground(Qt.green)
        reviewerFormat.setFontWeight(QFont.Black)
        self.reviewerRules = []
        for reviewer in reviewers:
            pattern = QRegExp("<\w*%s\w*>" % reviewer)
            rule = SyntaxHighlighter.HighlightingRule(pattern, reviewerFormat)
            self.reviewerRules.append(rule)

    def highlightBlock(self, text):
        self.highlightingRules = []
        self.highlightingRules.extend(self.basicRules)
        self.highlightingRules.extend(self.keywordsRules)
        self.highlightingRules.extend(self.reviewerRules)
        super(LogSyntaxHighlighter, self).highlightBlock(text)

def catCode(filePath, revision):
    fileName = filePath[filePath.rfind('/')+1:]
    tmpFileName = '/tmp/' + str(revision.number) + fileName
    tmpFile = open(tmpFileName, 'w+')
    svnClient = pysvn.Client()
    tmpFile.write(svnClient.cat(filePath, revision))
    return tmpFileName


class CodeHistoryViewer(QDialog, Ui_CodeHistoryViewer):
    def __init__(self, parent=None):
        super(CodeHistoryViewer, self).__init__(parent)
        self.setupUi(self)
        self.codeHistoryModel = CodeHistoryModel()
        self.codeHistoryFilterModel = CodeHistoryFilterProxyModel()
        self.codeHistoryFilterModel.setSourceModel(self.codeHistoryModel)
        self.revisions.setModel(self.codeHistoryFilterModel)
        self.revisions.setItemDelegate(HTMLDelegate())
        self.changedFileModel = ChangedFileModel()
        self.changedFiles.horizontalHeader().setResizeMode(QHeaderView.ResizeToContents)
        self.changedFiles.setModel(self.changedFileModel)
        self.changedFiles.setItemDelegate(HTMLDelegate())
        self.workingPath = ''
        self.rootUrl = ''
        self.logMessageHighlighter = LogSyntaxHighlighter(self.messages)


    def refresh(self, url):
        self.codeHistoryModel.refresh(url)
        self.codeHistoryFilterModel.reset()
        svnClient = pysvn.Client()
        self.rootUrl = svnClient.root_url_from_path(url)
        self.workingPath = url.replace(self.rootUrl, '')

    def on_revisions_pressed(self, modelIndex):
        commit = modelIndex.data(Qt.UserRole).toPyObject()
        self.changedFileModel.refresh(commit.changedPathsInfo(), self.workingPath,
                str(self.pathSearchEdit.text()).split())
        self.messages.setText(commit.message)

    def on_searchBtn_pressed(self):
        logSearchKeywords = str(self.logSearchEdit.text()).split()
        reviewerKeywords = str(self.reviewerSearchEdit.text()).split()
        self.codeHistoryFilterModel.setFilter(author = str(self.authorSearchEdit.text()),
                reviewers = reviewerKeywords,
                pathKeywords = str(self.pathSearchEdit.text()).split(),
                logKeywords = logSearchKeywords)
        self.logMessageHighlighter.highlightKeywords(logSearchKeywords)
        self.logMessageHighlighter.highlightReviewers(reviewerKeywords)

    def on_changedFiles_doubleClicked(self, modelIndex):
        filePath = str(self.rootUrl + modelIndex.data(Qt.UserRole).toPyObject())
        print filePath
        indexes = self.revisions.selectedIndexes()
        if not indexes:
            return
        commit = indexes[0].data(Qt.UserRole).toPyObject()
        codeFile = catCode(filePath, commit.revision)
        previousRevision = pysvn.Revision(pysvn.opt_revision_kind.number, int(commit.revision.number)-1)
        previousCodeFile = catCode(filePath, previousRevision)
        return os.system("meld %s %s" % (previousCodeFile, codeFile))



