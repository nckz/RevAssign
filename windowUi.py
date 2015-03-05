# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created: Fri Oct 12 15:31:31 2012
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(825, 651)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.catlist = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.catlist.sizePolicy().hasHeightForWidth())
        self.catlist.setSizePolicy(sizePolicy)
        self.catlist.setBaseSize(QtCore.QSize(200, 500))
        self.catlist.setAlternatingRowColors(True)
        self.catlist.setRootIsDecorated(False)
        self.catlist.setAllColumnsShowFocus(True)
        self.catlist.setObjectName(_fromUtf8("catlist"))
        self.catlist.header().setDefaultSectionSize(100)
        self.revlist = QtGui.QTreeWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.revlist.sizePolicy().hasHeightForWidth())
        self.revlist.setSizePolicy(sizePolicy)
        self.revlist.setBaseSize(QtCore.QSize(500, 500))
        self.revlist.setToolTip(_fromUtf8(""))
        self.revlist.setAlternatingRowColors(False)
        self.revlist.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.revlist.setRootIsDecorated(False)
        self.revlist.setObjectName(_fromUtf8("revlist"))
        self.revlist.header().setCascadingSectionResizes(False)
        self.revlist.header().setDefaultSectionSize(100)
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 825, 20))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuSorting = QtGui.QMenu(self.menubar)
        self.menuSorting.setObjectName(_fromUtf8("menuSorting"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpenSpreadsheet = QtGui.QAction(MainWindow)
        self.actionOpenSpreadsheet.setObjectName(_fromUtf8("actionOpenSpreadsheet"))
        self.actionOpenSession = QtGui.QAction(MainWindow)
        self.actionOpenSession.setObjectName(_fromUtf8("actionOpenSession"))
        self.actionSaveSession = QtGui.QAction(MainWindow)
        self.actionSaveSession.setObjectName(_fromUtf8("actionSaveSession"))
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName(_fromUtf8("actionExport"))
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName(_fromUtf8("actionQuit"))
        self.actionReviewerChoice = QtGui.QAction(MainWindow)
        self.actionReviewerChoice.setCheckable(True)
        self.actionReviewerChoice.setChecked(True)
        self.actionReviewerChoice.setWhatsThis(_fromUtf8(""))
        self.actionReviewerChoice.setObjectName(_fromUtf8("actionReviewerChoice"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionWorkflow = QtGui.QAction(MainWindow)
        self.actionWorkflow.setObjectName(_fromUtf8("actionWorkflow"))
        self.actionColorize = QtGui.QAction(MainWindow)
        self.actionColorize.setCheckable(True)
        self.actionColorize.setChecked(True)
        self.actionColorize.setObjectName(_fromUtf8("actionColorize"))
        self.actionAbstractLimit = QtGui.QAction(MainWindow)
        self.actionAbstractLimit.setObjectName(_fromUtf8("actionAbstractLimit"))
        self.menuFile.addAction(self.actionOpenSpreadsheet)
        self.menuFile.addAction(self.actionOpenSession)
        self.menuFile.addAction(self.actionSaveSession)
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuSorting.addAction(self.actionReviewerChoice)
        self.menuSorting.addAction(self.actionColorize)
        self.menuSorting.addAction(self.actionAbstractLimit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionWorkflow)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSorting.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.catlist.setStatusTip(QtGui.QApplication.translate("MainWindow", "select a category to assign reviewers", None, QtGui.QApplication.UnicodeUTF8))
        self.catlist.setSortingEnabled(True)
        self.catlist.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Category #", None, QtGui.QApplication.UnicodeUTF8))
        self.catlist.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Category Title", None, QtGui.QApplication.UnicodeUTF8))
        self.catlist.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "# of Abstracts", None, QtGui.QApplication.UnicodeUTF8))
        self.catlist.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "# of Assigned Reviewers", None, QtGui.QApplication.UnicodeUTF8))
        self.catlist.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "Pool Size", None, QtGui.QApplication.UnicodeUTF8))
        self.catlist.headerItem().setText(5, QtGui.QApplication.translate("MainWindow", "Assigned Reviewers", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.setStatusTip(QtGui.QApplication.translate("MainWindow", "check reviewers to assign them to the selected category", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.setSortingEnabled(True)
        self.revlist.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "Member #", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(1, QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(2, QtGui.QApplication.translate("MainWindow", "First", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(3, QtGui.QApplication.translate("MainWindow", "Last", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(4, QtGui.QApplication.translate("MainWindow", "Designation", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(5, QtGui.QApplication.translate("MainWindow", "Institution", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(6, QtGui.QApplication.translate("MainWindow", "Email", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(7, QtGui.QApplication.translate("MainWindow", "Primary Training", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(8, QtGui.QApplication.translate("MainWindow", "Pubmed", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(9, QtGui.QApplication.translate("MainWindow", "Pubmed #", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(10, QtGui.QApplication.translate("MainWindow", "Journal Articles", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(11, QtGui.QApplication.translate("MainWindow", "Reviewed Previously", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(12, QtGui.QApplication.translate("MainWindow", "Choice 1", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(13, QtGui.QApplication.translate("MainWindow", "Choice 2", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(14, QtGui.QApplication.translate("MainWindow", "Choice 3", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(15, QtGui.QApplication.translate("MainWindow", "Choice 4", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(16, QtGui.QApplication.translate("MainWindow", "Choice 5", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(17, QtGui.QApplication.translate("MainWindow", "# of Assigned Abstracts", None, QtGui.QApplication.UnicodeUTF8))
        self.revlist.headerItem().setText(18, QtGui.QApplication.translate("MainWindow", "Assigned Categories", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSorting.setTitle(QtGui.QApplication.translate("MainWindow", "Sorting", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenSpreadsheet.setText(QtGui.QApplication.translate("MainWindow", "Open Spreadsheet (.xls)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenSession.setText(QtGui.QApplication.translate("MainWindow", "Open Session (.mpc)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSaveSession.setText(QtGui.QApplication.translate("MainWindow", "Save Session (.mpc)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(QtGui.QApplication.translate("MainWindow", "Export (.xls)", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReviewerChoice.setText(QtGui.QApplication.translate("MainWindow", "Reviewer\'s Choice", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReviewerChoice.setToolTip(QtGui.QApplication.translate("MainWindow", "Reviewer\'s Choice", None, QtGui.QApplication.UnicodeUTF8))
        self.actionReviewerChoice.setStatusTip(QtGui.QApplication.translate("MainWindow", "sort based off of the reviwer\'s top 5 category choices", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionWorkflow.setText(QtGui.QApplication.translate("MainWindow", "Typical Workflow", None, QtGui.QApplication.UnicodeUTF8))
        self.actionColorize.setText(QtGui.QApplication.translate("MainWindow", "Colorize Rev. Choices", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbstractLimit.setText(QtGui.QApplication.translate("MainWindow", "Rev. Abstract Limit", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

