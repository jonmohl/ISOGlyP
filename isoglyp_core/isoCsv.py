import sys

class CSVReader:

    def __init__(self,inFile,sep=',',header=True,rowFilter=lambda x: True,skipLines=0,verbose=False,colTypes=None):
        ''' Read a .csv file into a list of lists. 

        inFile can be None, a filename, or a file-like object. If
        it is None, an empty CSV with no rows is created. In
        the other cases, the data is loaded from the file.

        sep is the column-separator character. '\t' is the one to
        use for tab-separated files.

        If header==True, assume the first row contains column headers. If
        header is a list, the members of the list will be converted to
        strings and used as the column names. If header is False or None,
        the column names will be simple integers starting at "1".
        
        rowFilter, if specified, should be a predicate that returns
        False only for rows that should be excluded from the
        dataset. The argument is the row data to be checked for
        exclusion, as a map of column name to value. 

        If skipLines is >0, ignore that number of beginning lines
        of the file. This can be used (perhaps in conjunction with
        header) to ignore comment lines at the start of the file
        that do not contain header information.

        If colTypes is supplied, it must be a map of column names or
        indices to a type-conversion function, eg int or str. All
        values are stored as strings unless otherwise converted.
        You can also convert column values after construction by
        using the setColumnTypes() method. In either case, all the
        data for the indicated columns is converted to the specified
        type immediately.
        '''
        if inFile is None:
            self.rows=[]
            self.colmap={}
            self.colNames=[]
            return
        if hasattr(inFile,'readlines'):
            inf = inFile
        else:
            inf=open(inFile,"r")
        result=map(lambda line: map(lambda x: x.strip(),line.split(sep)),inf.readlines())

        if verbose: print("bbrcCsv: len(results)=%s"%(len(result)))
        self.colmap={}
        if skipLines>0:
            result[:skipLines]=[]
        if header==True:
            self.colNames=self.fixDups(result[0])
            result[:1]=[]
        if type(header)==list:
            # Header is a list of column names.
            self.colNames=header[:]
        if not header:
            self.colNames=map(str,range(1,len(result[0])+1))
        self.colmap=dict(zip(self.colNames,range(len(self.colNames))))

        def filterProc(x):
            ''' Nested function to provide a filter framework. '''
            if len(x) != len(self.colNames):
                return False
            if rowFilter(dict(zip(self.colNames,x))):
                return True
            else:
                if verbose: print("Throwing away row %s"%(x,))
                return False

        result=filter(filterProc,result)
        self.rows = result
        self.columnTypes = {}
        self.setColumnTypes(colTypes)

    def emptyCopy(self):
        ''' Make a data set of the same shape (column names) as this
        one, but with no rows. '''
        return self.copy(copyRows=False) 

    def setColumnTypes(self,colTypes,reportErrors=False):
        '''
        Convert columns to specified types. colTypes must be a map
        of column name or index to type-conversion functions such
        as int. We attempt to convert each cell of each specified
        column to the indicated type by calling the associated
        conversion function. If the conversion fails, the value
        is silently left unchanged; unless reportErrors=True,
        in which case the conversion exception is thrown out
        of this method.
        '''
        if colTypes is None: return
        ctMap={}
        for col in colTypes.keys():
            if type(col)==int:
                ctMap[col]=colTypes[col]
            if type(col)==str:
                ctMap[self.colNames.index(col)]=colTypes[col]
        self.columnTypes.update(ctMap)
        for row in self.rows:
            for col in ctMap.keys():
                try:
                    row[col]=ctMap[col](row[col])
                except:
                    if reportErrors: raise

    def copy(self,copyRows=True):
        '''
        Return a deep copy of this CSV data set.
        '''
        cpy=CSVReader(inFile=None)
        cpy.colNames=self.colNames[:]
        cpy.columnTypes=self.columnTypes.copy()
        cpy.colmap=dict(zip(self.colNames,range(len(self.colNames))))
        cpy.rows=[]
        if copyRows:
            for row in self.rows:
                cpy.rows.append(row[:])
        return cpy

    def getColNames(self):
        ''' Return the column names of the table. '''
        return self.colNames

    def deleteColumn(self,colNameOrIdx):
        ''' Delete the given column, which may be specified by name or index. '''
        if type(colNameOrIdx) == int:
            colIdx=colNameOrIdx
        else:
            try:
                colIdx=self.colNames.index(colNameOrIdx)
            except ValueError:
                print>>sys.stderr, "No such column %s"%colNameOrIdx
                print>>sys.stderr, "In columns %s"%(self.colNames,)
                raise
        self.colNames=self.colNames[:colIdx]+self.colNames[colIdx+1:]
        newRows=[]
        for row in self.rows:
            newRows.append(row[:colIdx]+row[colIdx+1:])
        self.rows=newRows
        self.colmap=dict(zip(self.colNames,range(len(self.colNames))))

    def addRow(self,row):
        ''' Add a row to the data set. It can either be a list
            containing the new row values in the same order as
            the column headers for this data set, or else a
            dictionary mapping known column names to values. '''
        if type(row) == dict:
            self.addRowFromDict(row)
        else:
            while len(row) < len(self.colNames):
                row.append(None)
            self.rows.append(row)

    def addRowFromDict(self,rd):
        ''' Add a row to the data set from a dictionary of
            column names to values. Columns not present in
            the dictionary will be set to None. Unknown
            columns in the dictionary will be ignored. '''
        row=[None] * len(self.colNames)
        for kk in rd.keys():
            try:
                ii = self.colNames.index(kk)
                row[ii] = rd[kk]
            except ValueError:
                continue
        self.rows.append(row)

    def setRowVal(self,row,colName,value):
        ''' Set the value of a given row and column name.
            The row must be a list of values with the same
            shape as the colums of this data set. '''
        idx = self.colmap[colName]
        row[idx]=value

    def filterColumns(self,cols):
        ''' Return a copy of this table with the given columns removed. '''
        cpy=self.copy()
        for col in cols:
            cpy.deleteColumn(col)
        return cpy

    def keepRows(self,filterProc):
        ''' Keep rows for which filterProc returns True. The argument
        to filterProc is a map of column names to values. '''
        def filt(x):
            x=dict(zip(self.colNames,x))
            return filterProc(x)
        self.rows = filter(filt,self.rows)

    def addColumn(self,cname,cval):
        ''' Add a column to the right of the table and assign the given
        cval as the default value for every row. If the column already
        exists, do nothing and return False; otherwise, return True. '''
        if cname in self.colNames:
          return False
        self.colNames.append(cname)
        for row in self.rows:
            row.append(cval)
        self.colmap=dict(zip(self.colNames,range(len(self.colNames))))
        return True

    def reshape(self,colNames):
        ''' Ensure this has exactly the column names in colNames. Delete
            any column not in colNames, and add any column that isn't
            already present as an empty column. '''
        myCols = self.getColNames()
        for col in colNames:
            if col not in myCols:
                self.addColumn(col,"")
        for col in myCols:
            if col not in colNames:
                self.deleteColumn(col)

    def sort(self,cols):
        ''' 
        Sort the rows by the given columns, in order. You probably want to use
        setColumnTypes() before using this method.
        Each member of cols can be
          1) An int, in which case the sort is done by the column with that index.
             If the column index is negative, the sort will be in descending order.
          2) A column name, in which case the sort is done on the named column.
          3) A (name,direction) tuple, where direction is either 1 or -1. The
             sort is done on the named column, and in ascending order if direction
             is 1, or descending order if direction is -1.
        '''

        def sgn(n):
            ''' Return -1 for negative numbers, 1 for non-negative. '''
            if n<0: return -1
            return 1

        def makeComparator(idx,direction):
            ''' Make a comparator that sorts a selected column in a specific direction.'''
            if direction<0:
                ''' Descending order. '''
                def cmp(r1,r2):
                    if r1[idx]<r2[idx]: return 1
                    if r1[idx]>r2[idx]: return -1
                    return 0
            else:
                def cmp(r1,r2):
                    ''' Ascending order. '''
                    if r1[idx]>r2[idx]: return 1
                    if r1[idx]<r2[idx]: return -1
                    return 0
            return cmp

        idxs=[]
        for col in cols:
            if type(col)==str:
                direction=1
                if col[0]=='-':
                    col=col[1:]
                    direction = -1
                idx=self.colNames.index(col)
                idxs.append(makeComparator(idx,direction))
            if type(col)==int:
                idxs.append(makeComparator(col,sgn(col)))
            if type(col)==tuple:
                (col,direction)=col
                idxs.append(makeComparator(col,direction))

        def compare(r1,r2):
            ''' Comparator function that sorts according to the selected columns. '''
            for cmp in idxs:
                rc=cmp(r1,r2)
                if rc != 0: return rc
            return 0

        self.rows.sort(compare)

    def fixDups(self,lst):
        ''' Disambiguate identically-named columns by adding
            a unique digit to the name. '''
        lst=lst[:]
        for ii in range(1,len(lst)):
            disambig=1
            origVal=lst[ii]
            while lst[ii] in lst[:ii]:
                lst[ii]='%s_%s'%(origVal,disambig)
                disambig+=1
        return lst

    def getColumnMap(self):
        ''' Return a map of column name to column index. '''
        return self.colmap

    def getRow(self,idx):
        ''' Return a particular row, as a column->value map. '''
        return dict(zip(self.colNames,self.rows[idx]))

    def rowsAsMaps(self):
        ''' Iterate over rows, each as a column->value map. '''
        for row in self.rows:
            yield self.mapRow(row)
        return

    def mapRow(self,rowList,colNames=None):
        ''' Convert a row (list of values) into a map of column-name
        to value. '''
        if colNames is None:
            colNames = self.colNames
        return dict(zip(colNames,rowList))

    def rowsAsLists(self,columns=None):
        ''' Iterate over rows, each as a simple list of values. If
            columns is not None, return only the indicated columns
            for each row, in order. '''
        for row in self.rows:
            row = self.reorderRow(row,columns)
            yield row
        return

    def reorderRow(self,row,colNames):
        ''' Order the given row, which must be of the same shape
            as this data set, per the colNames list. The result
            will contain only the values of the indicated columns,
            in order. '''
        if colNames is None:
            return row
        rowMap = self.mapRow(row)
        result = []
        for col in colNames:
            result.append(rowMap[col])
        return result

    def getRawRow(self,idx):
        ''' Get a specified row as a simple list of values. '''
        return self.rows[idx]

    def nRows(self):
        ''' Return the number of rows in the table. '''
        return len(self.rows)

    def write(self,outf):
        ''' Write out the table as a comma-separated text file. '''
        outf.write(",".join(self.colNames))
        outf.write('\n')
        for row in self.rows:
            outf.write(",".join(map(str,row)))
            outf.write('\n')

if __name__=='__main__':
    # When run as a main script, this does some cool stuff that
    # I can't remember right now. Lets you filter columns and
    # rows with a simple predicate language.

    def intsWherePossible(colSpecs):
        ''' Convert each member of colSpecs to int if possible,
        otherwise leave it alone. '''
        cols=[]
        for cs in colSpecs:
            try:
               cols.append(int(cs))
            except ValueError:
               cols.append(cs) 
        return cols

    def buildFilter(specs):
        specs=specs.split(',')
        filters=[]
        for spec in specs:
            toks=spec.split(':')
            col=toks[0]
            val=toks[2]
            op=toks[1]
            valType=str
            if len(toks)>3:
                valType = eval(toks[3])
            if op == '==':
                # Note: need default args here because the variables
                # we are closing over may change.
                def flt(x,col=col,value=val,valType=valType): return x[col] == valType(value)
            if op == '!=':
                def flt(x,col=col,value=val,valType=valType): return x[col] != valType(value)
            if op == '<':
                def flt(x,col=col,value=val,valType=valType): return x[col] < valType(value)
            if op == '<=':
                def flt(x,col=col,value=val,valType=valType): return x[col] <= valType(value)
            if op == '>':
                def flt(x,col=col,value=val,valType=valType): return x[col] > valType(value)
            if op == '>=':
                def flt(x,col=col,value=val,valType=valType): return x[col] >= valType(value)
            filters.append(flt)
        def filterProc(x):
            for fp in filters:
                if not fp(x):
                    return False
            return True
        return filterProc

    import optparse
    ops=optparse.OptionParser()
    ops.add_option("--delete-cols",dest="dcols",default=None)
    ops.add_option("--sort",dest="sort",default=None)
    ops.add_option("--int-cols",dest="intcols",default=None)
    ops.add_option("--float-cols",dest="floatcols",default=None)
    ops.add_option("--filter",dest="filter",default=None)
    (opts,args) = ops.parse_args()
   
    inFile=args[0]
    csv=CSVReader(inFile,header=True,sep=',')

    if opts.intcols is not None:
        cols=intsWherePossible(opts.intcols.split(','))
        imap={}
        for col in cols:
            imap[col]=int
        csv.setColumnTypes(imap)
    if opts.floatcols is not None:
        cols=intsWherePossible(opts.floatcols.split(','))
        fmap={}
        for col in cols:
            fmap[col]=float
        csv.setColumnTypes(fmap)
    if opts.filter is not None:
        filterProc=buildFilter(opts.filter)
        csv.keepRows(filterProc)
    if opts.dcols is not None:
        cols=intsWherePossible(opts.dcols.split(','))
        csv=csv.filterColumns(cols)
    if opts.sort is not None:
        csv.sort(intsWherePossible(opts.sort.split(',')))

    csv.write(sys.stdout)
 
