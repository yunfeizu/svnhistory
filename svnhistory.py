#! /usr/bin/env python
# Copyright (C) 2012 Yunfei Zu <zuyunfei@gmail.com>

from PyQt4 import *
from svnhistory.CodeHistoryViewer import *
from svnhistory.RepositoryBrowser import *
import sys
import os

def main():
    app = QApplication(sys.argv)
    repositoryBrowser = RepositoryBrowser(os.getcwd())
    repositoryBrowser.show()
    app.exec_()

if __name__ == "__main__":
    main()
