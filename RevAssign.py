#!/usr/bin/env python
"""
    Author: Nicholas Zwart, Jim Pipe
    Date: 2011dec19

    Summary: User interface for the ISMRM AMPC Reviewer Assignment app.

    Specifications:
        http://www.ismrm.org/12/7T.pdf

    References:
        "PyQt by Example"
        http://lateral.netmanagers.com.ar/stories/BBS47.html

"""
__authors__ = ["Nick Zwart","Jim Pipe"]
__date__   = "2011dec19"

import os
import sys
import time
sys.path.insert(0, '../')

# Import Qt modules
from PyQt4 import QtCore,QtGui

# Import the compiled UI module
from RevAssign.windowUi import Ui_MainWindow

# Import the backend data containers
from RevAssign import backend


# correct the numeric sorting for specified columns of the category list
class cat_TreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent=None):
        QtGui.QTreeWidgetItem.__init__(self, parent)

    def __lt__(self, otherItem):
        column = self.treeWidget().sortColumn()

        if column == 2 or column == 3 or column == 4:
            return float( self.text(column) ) < float( otherItem.text(column) )
        elif column == 0:
            cur_s   = str(self.text(column))
            other_s = str(otherItem.text(column))
            cur_l = None # A or B
            other_l = None # A or B

            # get the underlying number for current
            if cur_s.isdigit():
                cur = float( cur_s )  
            else:
                cur_l = cur_s[-1] # remove letter
                cur = float( cur_s[0:-1] )  
                
            # get the underlying number for other
            if other_s.isdigit():
                other = float( other_s )  
            else:
                other_l = other_s[-1] # remove letter
                other = float( other_s[0:-1] )  
 
            # compare letters if they have the same base
            if cur == other:
                return cur_l < other_l
            else:
                return cur < other

        else:
            return self.text(column) < otherItem.text(column)


# correct the numeric sorting for specified columns of the reviewer list
class rev_TreeWidgetItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent=None, parent_obj=None):
        QtGui.QTreeWidgetItem.__init__(self, parent)

        # ref to parent class
        self.parent = parent_obj

        # if contents passed then decorate for sorting
        self.dlist = []
        self.dlist.append(int(parent[0])) # member #
        for i in xrange(1,12):
            self.dlist.append(str(parent[i]))
        for i in xrange(12,18):
            self.dlist.append(int(parent[i]))
        self.dlist.append(str(parent[18]))

        # color
        c1 = 240
        c2 = 230
        c3 = 220
        c4 = 210
        c5 = 200
        self.hghlghtColor = [QtGui.QColor(255,255,255),QtGui.QColor(c1,c1,c1),QtGui.QColor(c2,c2,c2),QtGui.QColor(c3,c3,c3),QtGui.QColor(c4,c4,c4),QtGui.QColor(c5,c5,c5),QtGui.QColor(128,0,0,alpha=128)]

        # set columns to be colorized based on sort
        self.totalCol = self.parent.ui.revlist.columnCount()
        self.firstcol = 1 # zero column doesn't work for some reason
        self.colRange = range(self.firstcol,self.totalCol)

        # choice column range
        #   -choices are in columns 12,13,14,15,16
        self.choices = range(12,17)

        # current color
        #   0:white, 1:light grey, ... 5:dark grey
        self.cur_color = 0
        self.new_color = 0

        # get handle to header and tree widgets
        self.tw = self.parent.ui.revlist
        self.hdr= self.parent.ui.revlist.header()


        self.getZeroColBrush()
        self.setAllBrushes()

    def getZeroColBrush(self):
        self.brush = self.background(0)

    def setAllBrushes(self):
        '''propagates colors to other items'''
        # set all other brushes to the same one
        self.brush = self.background(1)

        #for col in self.colRange:
        for col in xrange(0,self.totalCol):
            self.setBackground(col,self.brush)


    def __lt__(self, otherItem):

        # faster column refs
        # this would be faster if sortCol and sortInd could be known prior to __lt__()
        column = self.tw.sortColumn()
        sortInd = self.hdr.sortIndicatorOrder()

        # if the key exists
        if self.parent.cur_catkey and self.parent.rev_sortByChoice:

            # regardless of chosen column to sort on, always push common categories to the top
            # first check current item
            match_cur = False
            choice_cur = -1
            for i in self.choices:
                if float(self.text(i)) == self.parent.cur_catkey_num:
                    choice_cur = i
                    self.new_color = i-11
                    match_cur = True
                    break # no need to check the rest

            # second check other item
            match_other = False
            choice_other = -1
            for i in self.choices:
                if float(otherItem.text(i)) == self.parent.cur_catkey_num:
                    choice_other = i
                    otherItem.new_color = i-11
                    match_other = True
                    break # no need to check the rest

            # if they both have matches then sort by choice
            if match_cur and match_other:

                if choice_other == choice_cur:

                        # normal sorting
                        if column == 0 or column == 12 or column == 13 or column == 14 or column == 15 or column == 16 or column == 17:
                            return float( self.text(column) ) < float( otherItem.text(column) )
                        else:
                            return self.text(column) < otherItem.text(column)
                else:
                    # sort on choice prio
                    if sortInd == 0:
                        return choice_cur < choice_other
                    else:
                        return choice_cur > choice_other

            # if one of them matches then it is the priority
            if match_cur or match_other:
                # always put category sorting on top
                if sortInd == 1:
                    return match_cur < match_other
                else:
                    return match_cur > match_other

        # reset to white
        self.new_color = 0
        otherItem.new_color = 0

        # normal sorting
        if column == 0 or column == 12 or column == 13 or column == 14 or column == 15 or column == 16 or column == 17:
            return float( self.text(column) ) < float( otherItem.text(column) )
        else:
            return self.text(column) < otherItem.text(column)

# Create a class for our main window
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # This is always the same
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        # initialize window title
        self.setWindowTitle('ISMRM AMPC Reviewer Assignments') 
        self.status = self.ui.statusbar # get handle
        self.progress = QtGui.QProgressBar(self.statusBar())
        self.status.addPermanentWidget(self.progress)
        self.hide_progress_bar()

        # init the local data        
        # instantiate a local copy of the AMPC-chair workbook data
        self.chair = backend.AMPCchair_data()
        self.rev_items = [] # list of all item refs
        self.cat_items = [] # list of all item refs
        self.cur_cat_item = None # the cat item currently checked
        self.disableRevItemChanged = False
        self.disableCatItemChanged = False
        self.sessionActive = False
        self.cur_catkey = None
        self.cur_catkey_num = None # for speeding up sort
        self.cur_revkey = None
        self.rev_sortByChoice = True
        self.rev_colorized = True
        self.cur_rev_sortIndicator = 0
        self.rev_header = self.ui.revlist.header()
        self.rev_abs_warnThresh = 60

        QtCore.QObject.connect(self.ui.revlist.header(), QtCore.SIGNAL("sortIndicatorChanged()"),self.revlist_header_sortIndicatorChanged)

        # default column
        self.cur_rev_col = 1
        self.cur_cat_col = 1

        self.sortMsg = 'sorting items...'

        # speedups
        #self.ui.catlist.scheduleDelayedItemsLayout()
        #self.ui.revlist.scheduleDelayedItemsLayout()

        # status
        self.update_status('ready')

    def setCurCatKey(self,string):
        '''set key and numeric equiv'''

        # set current dictionary key
        self.cur_catkey = string

        # change key to digit 
        if self.cur_catkey.isdigit():
            self.cur_catkey_num = int(float(self.cur_catkey))
        else:
            # strip off A or B suffix
            self.cur_catkey_num = int(float(self.cur_catkey[0:-1]))


    def loadItems(self):

        self.update_status('loading items...')

        # don't draw new info to screen
        self.disableListUpdates()
    
        # init the list widget for reviewer info
        for k in self.chair.reviewers.iterkeys():

            # create item from row info based on key
            item = self.createRevItem(k)

            # init to unchecked, adds an unchecked box to the left of each entry
            item.setCheckState(0,QtCore.Qt.Unchecked)

            # place item in widget list
            self.ui.revlist.addTopLevelItem(item)

        # select this one
        self.ui.revlist.setItemSelected(item,1)

        # init the list widget for category info
        for k in self.chair.categories.iterkeys():

            # create item from row info
            item = self.createCatItem(k)

            # init to unchecked, adds an unchecked box to the left of each entry
            item.setCheckState(0,QtCore.Qt.Unchecked)

            # place item in widget list
            self.ui.catlist.addTopLevelItem(item)

        # select this one
        self.ui.catlist.setItemSelected(item,1)

        # build list of cat-item references
        cur_item = self.ui.catlist.itemAt(0,0)
        self.cat_items = [] # clear list before rebuild
        self.cat_items.append(cur_item)
        while self.ui.catlist.itemBelow(cur_item):
            cur_item = self.ui.catlist.itemBelow(cur_item)
            self.cat_items.append(cur_item)

        # build list of rev-item references
        cur_item = self.ui.revlist.itemAt(0,0)
        self.rev_items = [] # clear list before rebuild
        self.rev_items.append(cur_item)
        while self.ui.revlist.itemBelow(cur_item):
            cur_item = self.ui.revlist.itemBelow(cur_item)
            self.rev_items.append(cur_item)

        # do initial sort based on default column
        self.update_status(self.sortMsg)

        # sort categories first
        self.ui.catlist.sortItems(0,0)
        # select the first item
        cur_item = self.ui.catlist.itemAt(0,0)
        self.ui.catlist.setCurrentItem(cur_item)
        self.ui.catlist.setItemSelected(cur_item,self.cur_cat_col)
        # set the first item as cat_key
        self.setCurCatKey(str(cur_item.text(0)))
        self.disableCatItemChanged = True
        cur_item.setCheckState(0,QtCore.Qt.Checked)
        self.disableCatItemChanged = False
        self.cur_cat_item = cur_item #save this item for display updates (refreshDisplay())

        # make sure initial checkboxes are set
        self.disableRevItemChanged = True
        for item in self.rev_items:
            key = item.text(0) #reviewer keys from displayed rows

            # get associated cat list for current reviewer
            assoc = self.chair.reviewers[str(key)][18]

            # if the current cat matches any of the associated cat's
            # then mark as checked
            try:
                assoc.index(self.cur_catkey) # if it matches then continue
                item.setCheckState(0,QtCore.Qt.Checked)
            except:
                item.setCheckState(0,QtCore.Qt.Unchecked)
        self.disableRevItemChanged = False

        # now sort the revlist based on current selected cat_key
        self.ui.revlist.sortItems(0,0) # resort based on key
        # unselect any selected items
        items = self.ui.revlist.selectedItems() # loadItems()
        if len(items) > 0:
            items[0].setSelected(False) #unselect
        # select top item
        cur_item = self.ui.revlist.itemAt(0,0)
        self.ui.revlist.setCurrentItem(cur_item)
        self.ui.revlist.setItemSelected(cur_item,self.cur_rev_col)
        self.cur_revkey = str(cur_item.text(0))

        # redraw new info to screen
        self.enableListUpdates()

        # update item color
        self.refreshItemColor_rev()
 

    def deleteAllItems(self):
        '''Build lists and then use them to remove all items.'''
        
        # status
        self.update_status('clearing memory...')

        # this doesn't seem to correctly remove widget items
        #self.ui.revlist.clear()
        #self.ui.catlist.clear()

        self.disableListUpdates()
        self.update_status('clearing memory... (categories)')
        self.removeItemsFromList(self.ui.catlist,self.listItemsInTree(self.ui.catlist))
        self.update_status('clearing memory... (reviewers)')
        st = time.time()
        self.removeItemsFromList(self.ui.revlist,self.listItemsInTree(self.ui.revlist))
        print "revlist removal time: "+str(time.time()-st)
    
        self.enableListUpdates()

    def listItemsInTree(self,tree):
        # build list of cat-item references
        itemlst = []
        cur_item = tree.itemAt(0,0)
        itemlst.append(cur_item)
        while tree.itemBelow(cur_item):
            cur_item = tree.itemBelow(cur_item)
            itemlst.append(cur_item)
        return(itemlst)

    def refreshItemColor_rev(self):
        '''redraw item colors'''

        # stop list updates
        self.disableRevItemChanged = True
        self.ui.revlist.setDisabled(True)

        # status
        self.update_status(self.sortMsg)
        #cnt = float(self.ui.revlist.topLevelItemCount())
        cnt = len(self.rev_items)

        # go through all items
        # might have to get full list here first,
        # then update each item in the list
        i = 0
        for cur_item in self.rev_items:
            if self.rev_colorized:
                self.toggleColor(cur_item)
            else:
                self.setColorToWhite(cur_item)

            # status
            i += 1
            if i % 10 == 0:
                self.update_progress(i,cnt)

        self.status.clearMessage()
        self.hide_progress_bar()
        self.disableRevItemChanged = False
        self.ui.revlist.setDisabled(False)

    def update_progress(self, cur, total):
        self.progress.show()
        self.progress.setRange(0, total)
        self.progress.setValue(cur)
        QtGui.QApplication.processEvents() # allow gui to update

    def update_status(self, mesg):
        self.status.showMessage(mesg)
        QtGui.QApplication.processEvents() # allow gui to update

    def hide_progress_bar(self):
        self.progress.hide()
        QtGui.QApplication.processEvents() # allow gui to update

    def setHlght_AbsOverload(self,item):
        '''change color to light red if reviewer is or will be over the limit
           if added to current category
        '''
        item_key = str(item.text(0))

        # if the reviewer alone already has been assigned too many abs, then warn
        abs_total = float(self.chair.reviewers[item_key][17]) 
        if abs_total > self.rev_abs_warnThresh:
            col = 1
            item.setBackgroundColor(col,item.hghlghtColor[6])
            item.setAllBrushes()
            item.cur_color = 6
            return

        # first check that the item isn't already assigned to the current category
        # then warn if the rev's current abs total + current cat abs is too many
        try:
            self.chair.reviewers[item_key][18].index(self.cur_catkey)    
            return # don't do anything
        except:
            abs_total = float(self.chair.reviewers[item_key][17]) + float(self.chair.categories[self.cur_catkey][2])
            if abs_total > self.rev_abs_warnThresh:
                col = 1
                item.setBackgroundColor(col,item.hghlghtColor[6])
                item.setAllBrushes()
                item.cur_color = 6
            
    def setColorToWhite(self,item):
        '''change item color based on internal color flags'''
        # set to white
        item.new_color = 0
        # only address if needed
        if item.cur_color != item.new_color:
            # for each column, change the color 
            #for col in item.colRange:
            col = 1 
            #for col in item.colRange:
            item.setBackgroundColor(col,item.hghlghtColor[item.new_color])
            #item.brush.setColor(item.hghlghtColor[item.new_color])
            item.setAllBrushes()
            # set current color
            item.cur_color = item.new_color

        # check if warning should be set
        self.setHlght_AbsOverload(item)

    def toggleColor(self,item):
        '''change item color based on internal color flags'''
        # only address if needed
        if item.cur_color != item.new_color:
            # for each column, change the color 
            col = 1 
            #for col in item.colRange:
            item.setBackgroundColor(col,item.hghlghtColor[item.new_color])
            #item.brush.setColor(item.hghlghtColor[item.new_color])
            item.setAllBrushes()

            # set current color
            item.cur_color = item.new_color

        # check if warning should be set
        self.setHlght_AbsOverload(item)

    def removeItemsFromList(self,tree,inlist):
        print 'itemcnt:'+str(tree.topLevelItemCount())
        cnt = tree.topLevelItemCount()
        tree.clear()
        #for i in range(0,cnt):
        #    tree.takeTopLevelItem(0)
        #    self.update_progress(i,cnt)
        self.hide_progress_bar()

    # create a display item
    def createCatItem(self, key):
        '''write the category info to the QTreeWidgetItem '''
        # ensure each item is a string
        tmp_list = [ str(item) for item in self.chair.categories[key] ]

        # create an item for list in widget
        item = cat_TreeWidgetItem(tmp_list)

        return(item)

    # create a display item
    def createRevItem(self, key):
        '''write the reviewer info to the QTreeWidgetItem '''
        # ensure each item is a string
        tmp_list = [ str(item) for item in self.chair.reviewers[key] ]

        # create an item for list in widget
        item = rev_TreeWidgetItem(tmp_list,self)

        return(item)

    def on_catlist_itemChanged(self,cur=None,col=None):
        ''' set current key for category based on row selection '''
        if not self.sessionActive: return

        if self.disableCatItemChanged: return

        # only care if checkbox has changed
        if col == 0:

            print "catlist changed"

            # if it was unchecked, then re-check it
            if not cur.checkState(0):
                self.disableCatItemChanged = True
                cur.setCheckState(0,QtCore.Qt.Checked)
                self.disableCatItemChanged = False
                return

            # if the checkbox is selected
            if cur.checkState(0):
                # ensure that no other checkboxes are on
                # turn off all other non-selected boxes
                self.disableCatItemChanged = True
                for i in self.cat_items:
                    if i != cur:
                        i.setCheckState(0,QtCore.Qt.Unchecked)
                self.disableCatItemChanged = False

                # save current refs
                self.cur_cat_item = cur
                self.setCurCatKey(str(cur.text(0)))

                # prevent on_revlist_itemChanged() from triggering
                # don't update display
                self.disableRevItemChanged = True
                #self.disableListUpdates()
                self.ui.revlist.setDisabled(True)


                # whenever the category selection is changed,
                # the appropriate reviewers need to be checked.
                # So this will go through the items in QTreeWidget(revlist)
                # and compare to list in dict(categories), matching keys will 
                # cause checked boxes and non-matching will cause unchecked boxes
                st = time.time()
                for item in self.rev_items:
                    key = item.text(0) #reviewer keys from displayed rows

                    # get associated cat list for current reviewer
                    assoc = self.chair.reviewers[str(key)][18]

                    # if the current cat matches any of the associated cat's
                    # then mark as checked
                    try:
                        assoc.index(self.cur_catkey) # if it matches then continue
                        item.setCheckState(0,QtCore.Qt.Checked)
                    except:
                        item.setCheckState(0,QtCore.Qt.Unchecked)

                # initiate sort on current column using current ordering        
                if self.rev_sortByChoice:
                    st = time.time()
                    self.update_status(self.sortMsg)
                    self.ui.revlist.sortItems(self.ui.revlist.header().sortIndicatorSection(),self.ui.revlist.header().sortIndicatorOrder())
                    print "     -sort time: "+str(time.time()-st)

                    # select first item 
                    #cur_item = self.ui.revlist.itemAt(0,0)
                    #self.ui.revlist.setItemSelected(cur_item,self.ui.revlist.header().sortIndicatorSection())
                    #self.ui.revlist.setCurrentItem(cur_item)

                    # redraw color
                    st = time.time()
                    self.refreshItemColor_rev()
                    print "     -re-color time: "+str(time.time()-st)

                # allow update of display
                #self.enableListUpdates()
                self.ui.revlist.setDisabled(False)
                self.disableRevItemChanged = False

                # focus on first rev item
                # get current selected item
                items = self.ui.revlist.selectedItems() # on_catlist_itemChanged()
                if len(items) > 0:
                    items[0].setSelected(False) #unselect
                cur_item = self.ui.revlist.itemAt(0,0)
                self.ui.revlist.setItemSelected(cur_item,self.ui.revlist.header().sortIndicatorSection())
                self.ui.revlist.setCurrentItem(cur_item)


    def on_revlist_itemSelectionChanged(self):
        ''' set current key for reviewer based on row selection '''

        # check sort indicator status and store
        #self.cur_rev_sortIndicator = self.ui.revlist.header().sortIndicatorOrder()
        #self.cur_rev_col = self.ui.revlist.sortColumn()

        if self.sessionActive:
            items = self.ui.revlist.selectedItems()
            if len(items) > 0:# only one item selectable
                self.cur_revkey = str(items[0].text(0))

    def revlist_header_sortIndicatorChanged(self):#,section=None,order=None):
        print "revlist_header_sortIndicatorChanged triggered"
        #print section
        #print order

    def on_revlist_itemChanged(self,cur=None,col=None):
        ''' checkbox state change
             -item selection always happens first, even if
             -checkbox is checked on non-selected item '''

        # keep from processing display updates when revlist items are changed
        if self.disableRevItemChanged: return

        # check sort indicator status and store
        #self.cur_rev_sortIndicator = self.ui.revlist.header().sortIndicatorOrder()
        #self.cur_rev_col = self.ui.revlist.sortColumn()

        # only care if checkbox has changed
        if col == 0:
        #if True:

            # for debugging
            if str(cur.text(0)) == self.cur_revkey:
                print "spacebar used to select or mouse on highlighted row"
            else:
                # shouldn't this always be the case?
                self.cur_revkey = str(cur.text(0))
                print "mouse checked non-highlighted row"

            # if it IS checked
            if cur.checkState(0):

                # test category selection
                try:
                    self.chair.categories[self.cur_catkey]
                except:
                    print "ERROR: please choose a category"
                    return

                # test reviewer selection
                try:
                    self.chair.reviewers[self.cur_revkey]
                except:
                    print "ERROR: please choose a reviewer"
                    return

                print "item checked, col:"+str(col)
                self.chair.addRev(self.cur_revkey,self.cur_catkey)

            else:
                print "item not checked, col:"+str(col)
                self.chair.removeRev(self.cur_revkey,self.cur_catkey)

            # refresh row data
            self.refreshDisplay()

    def disableListUpdates(self):
        # disable list signals
        #self.ui.catlist.setUpdatesEnabled(False)
        #self.ui.revlist.setUpdatesEnabled(False)

        self.ui.catlist.setDisabled(True)
        self.ui.revlist.setDisabled(True)


    def enableListUpdates(self):
        # enable list signals
        #self.ui.catlist.setUpdatesEnabled(True)
        #self.ui.revlist.setUpdatesEnabled(True)

        self.ui.catlist.setDisabled(False)
        self.ui.revlist.setDisabled(False)

    def getItemFromRevKey(self,key):
        for item in self.rev_items:
            if item.text(0) == key:
                return item

    def refreshDisplay(self):
        '''update the new tallied items in each list
            i.e.:
            -number of abstracts
            -number of revs in this category
        '''

        # disable update of display
        self.disableRevItemChanged = True
        #self.disableListUpdates()


        # display cat
        #item_r = self.ui.catlist.selectedItems()[0]
        item_r = self.cur_cat_item
        # set # of assigned reviewers
        item_r.setText(3,self.chair.categories[self.cur_catkey][3])
        print item_r.text(3)
        # assigned reviewers
        item_r.setText(5,str(self.chair.categories[self.cur_catkey][5]))
        print item_r.text(5)

        # display rev
        #item_c = self.ui.revlist.selectedItems()[0]
        item_c = self.getItemFromRevKey(self.cur_revkey)
        # set # of assigned reviewers
        item_c.setText(17,self.chair.reviewers[self.cur_revkey][17])
        item_c.dlist[17] = int(self.chair.reviewers[self.cur_revkey][17])
        print item_c.text(17)
        # assigned reviewers
        item_c.setText(18,str(self.chair.reviewers[self.cur_revkey][18]))
        item_c.dlist[18] = str(self.chair.reviewers[self.cur_revkey][18])
        print item_c.text(18)

        # update color after tables have been modified
        self.toggleColor(item_c)

        # allow update of display
        #self.enableListUpdates()
        self.disableRevItemChanged = False

    def on_actionAbstractLimit_triggered(self,checked=None):
        # this always has to be checked for triggered actions
        # to keep from running double actions
        if checked is None: return

        text, ok = QtGui.QInputDialog.getText(self, 'Reviewer Abstract Warning Limit', 'Enter Limit (Cur:'+str(int(self.rev_abs_warnThresh))+'):')
        if ok:
            if str(text).isdigit():
                self.ui.revlist.setDisabled(True)
                self.rev_abs_warnThresh = float(text)
                print "rev_abs_warnThresh set to: "+str(self.rev_abs_warnThresh)
                self.refreshItemColor_rev()
                self.ui.revlist.setDisabled(False)

    def on_actionReviewerChoice_triggered(self,checked=None):
        '''toggle reviewer choice sorting'''
        # this always has to be checked for triggered actions
        # to keep from running double actions
        if checked is None: return

        # toggle sorting feature
        if checked: 
            self.rev_sortByChoice = True
        else:
            self.rev_sortByChoice = False 

        # update item color
        # something is interrupting the conversion back to white
        if self.sessionActive:
            self.ui.revlist.setDisabled(True)
            self.ui.revlist.sortItems(self.ui.revlist.header().sortIndicatorSection(),self.ui.revlist.header().sortIndicatorOrder())
            self.refreshItemColor_rev()
            self.ui.revlist.setDisabled(False)

    def on_actionColorize_triggered(self,checked=None):
        '''toggle reviewer choice sorting'''
        # this always has to be checked for triggered actions
        # to keep from running double actions
        if checked is None: return

        # toggle sorting feature
        if checked: 
            self.rev_colorized = True
        else:
            self.rev_colorized = False 

        # update item color
        # something is interrupting the conversion back to white
        if self.sessionActive:
            self.ui.revlist.setDisabled(True)
            self.ui.revlist.sortItems(self.ui.revlist.header().sortIndicatorSection(),self.ui.revlist.header().sortIndicatorOrder())
            self.refreshItemColor_rev()
            self.ui.revlist.setDisabled(False)

    def on_actionSaveSession_triggered(self,checked=None):
        # this always has to be checked for triggered actions
        # to keep from running double actions
        if checked is None: return

        # check if session is already active
        if not self.sessionActive:
            print "ERROR: no active session to save"
            return

        # open file browser
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Save Session (*.mpc)', os.path.expanduser('~/'), filter='AMPC Chair Session (*.mpc)')
        print fname

        # check for empty strings, if canceled
        if not fname:
            return

        # save window state
        state = []
        state.append(self.saveGeometry()) # main window
        state.append(self.ui.splitter.saveState()) # splitter

        # save session
        self.chair.writeSession(fname,state)

    def on_actionExport_triggered(self,checked=None):
        # this always has to be checked for triggered actions
        # to keep from running double actions
        if checked is None: return

        # check if session is already active
        if not self.sessionActive:
            print "ERROR: no active session to export"
            return

        # open file browser
        fname = QtGui.QFileDialog.getSaveFileName(self, 'Export Session (*.xls)', os.path.expanduser('~/'), filter='AMPC Chair Session (*.xls)')
        print fname

        # check for empty strings, if canceled
        if not fname:
            return

        # save session
        self.chair.writeSpreadsheet(fname)

    def on_actionOpenSession_triggered(self,checked=None):
        # this always has to be checked for triggered actions
        # to keep from running double actions
        if checked is None: return

        # open file browser
        fname = QtGui.QFileDialog().getOpenFileName(self, 'Open Session (*.mpc)', os.path.expanduser('~/'), filter='AMPC Chair Session (*.mpc)')
        print fname

        # check for empty strings, if canceled
        if not fname:
            return

        # check if session is already active
        if self.sessionActive:
            self.sessionActive = False
            self.deleteAllItems()
            self.update_status('clearing memory... (dictionaries)')
            self.chair.deleteAll()

        # read the file
        self.update_status('opening session...')
        if self.chair.readSession(fname) != 0:
            return

        # resize window to saved state
        if self.chair.state:
            print "restore mainwindow state:"
            print self.restoreGeometry(self.chair.state[0])
            print "restore splitter state:"
            print self.ui.splitter.restoreState(self.chair.state[1])

        # load display
        self.loadItems()

        # mark a session already in use
        self.sessionActive = True


    def on_actionOpenSpreadsheet_triggered(self,checked=None):
        # this always has to be checked for triggered actions
        # to keep from running double actions
        if checked is None: return

        # open file browser
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open Spreadsheet (*.xls)',os.path.expanduser('~/'), filter='AMPC Chair Session (*.xls)')
        print fname

        # check for empty strings, if canceled
        if not fname:
            return

        # check if session is already active
        if self.sessionActive:
            self.sessionActive = False
            self.deleteAllItems()
            self.update_status('clearing memory... (dictionaries)')
            self.chair.deleteAll()

        # read the file
        self.update_status('opening spreadsheet...')
        if self.chair.read(fname) != 0:
            return # no successful input

        # load display
        self.loadItems()

        # mark a session already in use
        self.sessionActive = True

    def on_actionQuit_triggered(self):
        QtGui.QApplication.closeAllWindows()

    def on_actionAbout_triggered(self,checked=None):
        if checked is None: return
        msg = "RevAssign was created to help the ISMRM AMPC Chair assign reviewers to categories.\n\n"+ \
            "\tAuthors: "+str(', '.join(__authors__))+"\n" \
            "\tDate: "+str(__date__)+"\n\n" \
            "URL: https://github.com/nckz/RevAssign#revassign"
        mb = QtGui.QMessageBox.about(self, "About RevAssign", msg)
             
    def on_actionWorkflow_triggered(self,checked=None):
        if checked is None: return
        mb = QtGui.QMessageBox()
        mb.setSizeGripEnabled(True) 
        mb.about(self,"Help", \
            "The ISMRM AMPC Chair interface is designed to help the chairperson assign reviewers to categories based on the reviewer's preferences, qualifications, publications, etc...  "+ \
            "The goal of this interface is to provide sorting and automatic accounting capabilities that allow these decisions to be made rapidly.  "+ \
            "The input required by this program is an Excel spreadsheet (.xls) returned by MIRA Digital Publishing containing the information of the online questionnaire that each reviewer filled out.  "+ \
            "The spreadsheet workbook must contain the reviewer information in the first sheet and category information in the second sheet, with column information as follows:  \n\n"+ \
            "Reviewers: [member #, type, first, last, designation, inst., email, training, pubmed, pubmed#, #articles, previously reviewed, choice1...5] "+ \
            "-the header row is skipped and any row that doesn't have a numeric member number.\n\n"
            "Categories: [category #, title, # of abstracts] "+ \
            "-the specific column labels are not important, the first header-row is skipped and the last abstract total row is skipped, categories may only be split into two (i.e. A & B).\n\n"+ \
            "A session simply consists of assigning reviewers to each category using the check boxes and the sorting capabilities embedded in each column header.  "+ \
            "The headers and spreadsheet panes can be resized.  The columns can also be moved left or right.  "+ \
            "If needed, the session can be saved and resumed later by saving to a .mpc file using the save session dialog.  "+ \
            "After all categories have been assigned, the final data are exported (via the Export dialog) back to an Excel spreadsheet with similar format to the input.")

def main():
    # Again, this is boilerplate, it's going to be the same on 
    # almost every app you write
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    window.raise_()
    # It's exec_ because exec is a reserved word in Python
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
    
