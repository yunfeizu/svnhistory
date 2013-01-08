svnhistory
==========

svn GUI tool to view code history efficiently


About
-----
* Authors:     Check the copyright notices in each source file
* License:     GNU General Public License Version 3

* Website:     https://github.com/yunfeizu/svnhistory
* Bug reports: https://github.com/yunfeizu/svnhistory/issues
* git clone    https://github.com/yunfeizu/svnhistory.git

Design Goals
------------
* An GUI to review code after commits
* An easily useful tool to track code changes in svn
* Fast response in searching and viewing log message
* Keep it small but useful, do one thing and do it well

Features
--------
* svn repository browser
* svn history viewer
* search svn history with author, reviewer, changed pathes or log message
* search keywords highlighting
* TODO: generate change report between builds or revisions for testers 
* TODO: generate review protocol for project management

Dependencies
------------
* Python 2.x (tested with version 2.7) 
* PyQt4 
* pysvn (ubuntu package python-svn)
* meld (text diff tool)

Installing
----------
To install svnhistory manually:
    sudo python setup.py install

tested on fedora 17 and ubuntu 12.04

Getting Started
---------------
TODO: add user guide here
