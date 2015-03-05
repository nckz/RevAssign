"""
   Author: Nicholas Zwart, Jim Pipe
   Date: 2011dec19

   Summary: Backend interface for AMPC Chair person's spreadsheet editing tasks.

"""

__authors__ = ["Nick Zwart","Jim Pipe"]
__date__   = "2011dec19"
__version__ = "r2832"

import xlrd # tools for reading spreadsheets
import xlwt # tools for writing spreadsheets
import pickle # for saving and opening sessions


class AMPCchair_data:
    '''Methods for storing and retrieving reviewer data and category data'''

    def __init__(self):
        self.rev_sheet = None # reviewer workbook info
        self.cat_sheet = None # category workbook info

        # window state
        self.state = None

        # load data from xls file
        #self.read_rev()
        #self.read_cat()
        #self.read()

    def deleteAll(self):
        '''remove all sheets and dictionaries from mem'''
        #del self.rev_sheet # these need to be unloaded properly
        #del self.cat_sheet
        del self.reviewers 
        del self.categories 

    def read_rev(self,fn='reviewer.xls'):
        '''read the spreadsheet data given the supplied Excel filename
        '''
        book = xlrd.open_workbook(fn)
        self.rev_sheet = book.sheets()[0] # only the first sheet
        return(self.rev_sheet) # return ref to sheet

    def read_cat(self,fn='category.xls'):
        '''read the spreadsheet data given the supplied Excel filename
        '''
        book = xlrd.open_workbook(fn)
        self.cat_sheet = book.sheets()[0] # only the first sheet
        return(self.cat_sheet) # return ref to sheet

    def format_catlist(self,inlist):
        '''take the input list, and enforce cell format
           -all are strings, member numbers and category choices should
            be changed to ints before strings
           -category number (some are ints and others are alpha-numeric), col 0
           -category name, col 1
           -num abs, col 2
        '''
        outlist = []
        # category number
        try:
            outlist.append(str(int(float(inlist[0]))))
        except:
            outlist.append(str(inlist[0]))
        # name
        outlist.append(str(inlist[1]))
        # num abstracts
        outlist.append(str(int(float(inlist[2]))))
        # add extra columns for # assigned revs, pool, and assigned revs if needed 
        while len(outlist) < 6:
            outlist.append(str(0))
        # set keylist to a list
        outlist[5] = []
        return(outlist)

    def format_revlist(self,inlist):
        '''take the input list, and enforce cell format
           -all are strings, member numbers and category choices should
            be changed to ints before strings
           -member number col 0
           -col 12:16 are choices
        '''
        outlist = []
        # member number
        outlist.append(str(int(float(inlist[0]))))
        # string info
        for i in range(1,12):
            
            # check all chars in each string
            if type(inlist[i]) == str or type(inlist[i]) == unicode:
                cell = []
                for c in inlist[i]:
                    try:
                        cell.append(str(c))
                    except:
                        pass #skip extra encoded chars
                cell = ''.join(cell)
                outlist.append(cell)
            else:
                outlist.append(str(inlist[i]))

        # choices
        for i in range(12,17):
            try:
                # for non-empty entries
                outlist.append(str(int(float(inlist[i]))))
            except:
                # for empty entries
                outlist.append('-1')
        # add extra columns for num abstracts and assigned cat
        while len(outlist) < 19:
            outlist.append(str(0))
        # set keylist to a list
        outlist[18] = []
        return(outlist)

    def read(self,fn): #='abstassn.xls'):
        '''read both reviewer and category sheets from a single book
        '''
        try:
            book = xlrd.open_workbook(fn)
        except:
            print 'ERROR: invalid xls file'
            return 1
        sheets = book.sheets()
        self.rev_sheet = sheets[0] # only the first sheet
        self.cat_sheet = sheets[1] # only the second sheet

        # REVIEWERS
        # make a dictionary for reviewers based on member number
        # number of reviewers, only count rows with member numbers
        #   -all numbers should be stored as float
        #   -any alphanumeric either unicode or string
        self.num_reviewers = 0
        self.reviewers = []
        bad_cnt = 0
        read_cnt = 0
        for i in range(0,self.rev_sheet.nrows):
            # filter out non-compliant rows
            try:
                mem_info = self.format_revlist(self.rev_sheet.row_values(i))
                self.num_reviewers += 1
                self.reviewers.append((mem_info[0],mem_info))
                read_cnt += 1
            except:
                bad_cnt += 1
                print 'bad_cnt:'+str(bad_cnt)
                print self.rev_sheet.row_values(i)
                #pass # just skip rows with no member number
        print "REVIEWERS: read:"+str(read_cnt)
        print "REVIEWERS: unreadable rows:"+str(bad_cnt)
        self.reviewers = dict(self.reviewers)

        # CATEGORIES
        # dictionary and number of categories, skip major category rows
        self.num_categories = 0
        self.categories = []
        bad_cnt = 0
        read_cnt = 0
        for i in range(0,self.cat_sheet.nrows): # drop last row
            # filter out non-compliant rows
            try:
                cur_row = self.format_catlist(self.cat_sheet.row_values(i))

                # Valid rows have category numbers that can be reduced to digits
                # if only one char is dropped from the end in the event of <cat>A
                # or <cat>B.
                # This will drop the main categories, header rows and abs-total rows.

                # check that the rule applies
                if cur_row[0].isdigit() or cur_row[0][0:-1].isdigit():
                    self.num_categories += 1

                    # zero-fill category numbers
                    # split categories are already strings so they
                    # are already zero filled
                    if cur_row[0].isdigit():
                        cur_row[0] = cur_row[0].zfill(3)

                    self.categories.append((cur_row[0],cur_row))
                    read_cnt += 1

                else:
                    bad_cnt += 1
                    print self.cat_sheet.row_values(i)

            except:
                # tally non-readable rows
                bad_cnt += 1
                print self.cat_sheet.row_values(i)
        print "CATEGORIES: read:"+str(read_cnt)
        print "CATEGORIES: unreadable/main-category rows:"+str(bad_cnt)
        self.categories = dict(self.categories)


        # calculate the number of reviewers for each cat
        self.calcReviewPools()

        return(0) # success

    def calcReviewPools(self):
        '''Each reviewer has chosen categories that they would like to review in columns 12,13,14,15,16 (0-based)
           Each category has a number, however, some are split (e.g. 900->900A & 900B).
           The split categories will get the same reviewer pool sum.  These categories need to be identified with 
           the correct number first.
        '''
        # for each reviewer
        for k,v in self.reviewers.iteritems():
            # for each choice
            for choice in v[12:17]:
                # determine if choice is empty
                if choice.isdigit():
                    # try the num, numA, and numB
                    # also add leading zeros, up to 2, 0 or 00
                    choices = [choice,choice+'A',choice+'B']
                    choices_00 = []
                    for c in choices:
                        choices_00.append(c)
                        choices_00.append('0'+c)
                        choices_00.append('00'+c)

                    # increment all matches
                    for c in choices_00:
                        try:
                            self.categories[c][4] = str(int(self.categories[c][4]) + 1)
                        except:
                            pass

    def addRev(self,cur_rev,cur_cat):
        '''add keys to each list and tally abstracts and reviewers for the 
           appropriate lists '''

        # swap keys
        self.reviewers[cur_rev][18].append(cur_cat)
        self.categories[cur_cat][5].append(cur_rev)

        # tally keys
        ## number of abstracts
        self.reviewers[cur_rev][17] = str( int(self.reviewers[cur_rev][17]) + int(self.categories[cur_cat][2]) )
        ## number of reviewers
        self.categories[cur_cat][3] = str(len(self.categories[cur_cat][5]))

    def removeRev(self,cur_rev,cur_cat):
        '''add keys to each list and tally abstracts and reviewers for the 
           appropriate lists '''

        # swap keys
        ind = self.reviewers[cur_rev][18].index(cur_cat)
        self.reviewers[cur_rev][18].pop(ind)
        ind = self.categories[cur_cat][5].index(cur_rev)
        self.categories[cur_cat][5].pop(ind)

        # tally keys
        ## number of abstracts
        self.reviewers[cur_rev][17] = str( int(self.reviewers[cur_rev][17]) - int(self.categories[cur_cat][2]) )
        ## number of reviewers
        self.categories[cur_cat][3] = str(len(self.categories[cur_cat][5]))

                        
    def incCat_PoolSize(self,cnum):
        '''checks to see if pool size column exists, 
           creates it if it doesn't and increments the value.
           -cnum is the category ref number key
           column 4, 0-based
        '''
        # get list
        item = self.categories[cnum]

        # grow the list (if needed)
        while len(item) < 5:
            item.append(0)

        # assign the value
        item[4] += 1

    def incCat_NumRev(self,cnum):
        '''checks to see if pool size column exists, 
           creates it if it doesn't and increments the value.
           -cnum is the category ref number key
           column 3, 0-based
        '''
        # get list
        item = self.categories[cnum]

        # grow the list (if needed)
        while len(item) < 4:
            item.append('')

        # assign the value
        item[3] = value

    def setRev_NumAbs(self,mem,value):
        '''checks to see if pool size column exists, 
           creates it if it doesn't and inserts the value.
           -mem is the reviewer number key 
           column 17, 0-based
        '''
        # get list
        item = self.reviewers[mem]

        # grow the list (if needed)
        while len(item) < 18:
            item.append('')

        # assign the value
        item[17] = value


    def get_rev_titles(self):
        '''get the column titles from rev info
           this is left open in case new reviewer info is added
        '''
        return(self.rev_sheet.row_values(0))

    def get_rev_info(self, num):
        '''get the reviewer info, 1-based to skip title'''
        if num <= self.rev_sheet.nrows:
            return(self.rev_sheet.row_values(num))

    def get_cat_info(self, num):
        '''get the category info, 1-based to skip title'''
        if num <= self.cat_sheet.nrows:
            return(self.cat_sheet.row_values(num))

    def get_nrev(self):
        '''number of rows -1 == num reviewers'''
        return(self.rev_sheet.nrows-1)

    def get_ncat(self):
        '''number of rows -1 == num categories'''
        return(self.cat_sheet.nrows-1)

    def writeSpreadsheet(self,fn):
        '''get dictionaries into proper spreadsheet format and write'''
        # init output book
        book = xlwt.Workbook()

        # REVIEWERS
        # make a sheet for reviewers
        sheet1 = book.add_sheet('Reviewers')
        
        # convert dict to list
        outlist = self.dict2List(self.reviewers)

        # copy list into sheet
        self.addRevHeader2Sheet(sheet1)
        self.list2Sheet(outlist,sheet1,1)

        # CATEGORIES
        # make a sheet for reviewers
        sheet2 = book.add_sheet('Categories')
        
        # convert dict to list
        outlist = self.dict2List(self.categories)

        # copy list into sheet
        self.addCatHeader2Sheet(sheet2)
        self.list2Sheet(outlist,sheet2,1)

        # write to file
        book.save(fn)

    def expandColumnList(self, li):
        '''Unwrap the elements of Assigned Reviewers & Assigned Categories into multiple columns'''
        row = []
        for elem in li:
            row.append(str(elem))
        return(row)

    def addRevHeader2Sheet(self,sheet_in):
        '''add the rev header row to supplied sheet'''
        head = ['Member #','Type','First','Last','Designation','Institution','Email','Primary Training','PubMed','PubMed #','Journal Articles','Previously Reviewed','Choice 1','Choice 2','Choice 3','Choice 4','Choice 5','# of Assigned Abstracts','Assigned Categories']
        row = 0
        for col in range(0,len(head)):
            sheet_in.write(row,col,head[col])
    
    def addCatHeader2Sheet(self,sheet_in):
        '''add the category header row to supplied sheet'''
        head = ['Category #','Category Title','# of Abstracts','# of Assigned Reviewers','Pool Size','Assigned Reviewers']
        row = 0
        for col in range(0,len(head)):
            sheet_in.write(row,col,head[col])

    def dict2List(self,dict_in):
        '''flatten dictionary elements to string elements in a list'''
        outlist = []
        for v in dict_in.itervalues():
            rowlist = []
            # ensure each element of a row is a string
            for i in v:
                rowlist.append( str(i) )

            # make lists individual cells
            rowlist.pop()
            rowlist += self.expandColumnList(v[-1])

            # append the row
            outlist.append(rowlist)
        return(outlist)

    def list2Sheet(self,list_in,sheet_in,row_offset):
        '''copy elems of list into sheet'''
        for row in range(0,len(list_in)):
            for col in range(0,len(list_in[row])):
                sheet_in.write(row+row_offset,col,list_in[row][col])

    def writeSession(self,fn,state=None):
        '''write dictionaries to supplied file'''
        # group data
        group = []
        group.append(['ISMRM AMPC Chair Session',str(__version__)]) # header list
        group.append(self.reviewers)
        group.append(self.categories)

        # state is elem 2 in header
        if state:
            group[0].append(state)
        else:
            group[0].append('no state info')

        # open file stream
        fileptr = open(fn,'wb')

        # write
        pickle.dump(group, fileptr)

        # close stream
        fileptr.close()

    def readSession(self,fn):
        '''read dictionaries from supplied file'''
        # open file stream
        fileptr = open(fn,'rb')

        # load data
        try:
            group = pickle.load(fileptr)
        except:
            print 'ERROR: invalid pickle file'
            fileptr.close()
            return 1

        # close stream
        fileptr.close()

        # load data into class
        hdr = group[0]
        if hdr[0] == 'ISMRM AMPC Chair Session':
            print 'valid ISMRM AMPC Chair Session found'
            print '\t-file created with version '+str(hdr[1])
            self.reviewers  = group[1]
            self.categories = group[2]
            if group[0][2] == 'no state info':
                self.state = None
            else:
                self.state = group[0][2] # window state
        else:
            print "ERROR: the chosen file is not an ISMRM AMPC Chair session"

        return 0




