""" SqlDataOut - class to produce SQL data command file output.

    $Id: sqldataout.py,v 1.2 2009/10/10 08:54:24 xavier Exp $
"""
__revision__ = "$Revision: 1.2 $"[11:-2]
__author__ = 'Reg. Charney <pymetrics@charneyday.com>'

import time
import PyMetrics.sqltemplate

class InvalidTableNameError( Exception ): 
    """ Used to indicate that the SQL table name is invalid."""
    pass

class SqlDataOut( object ):
    """ Class used to generate a command file suitable for runnning against
    any SQL dbms."""
    def __init__( self, 
                  fd, 
                  libName, 
                  fileName, 
                  tableName, 
                  genNewSw=False, 
                  genExistsSw=False ):
        """ Initialize instance of SqlDataOut."""
        if tableName == '':
            raise InvalidTableNameError( tableName )
        if not fd:
            raise IOError( "Output file does not yet exist" )
            
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.libName = libName
        self.fileName = fileName
        self.tableName = tableName
        self.quotedFileName = '"'+self.fileName+'"'
        self.IDDateTime = '"'+timestamp+'"'
        self.datanum = 0
        self.fd = fd
        
        if not genExistsSw:
            self.writeHdr( genNewSw, tableName )
        
    def writeHdr( self, genNewSw, tableName ):
        """ Write header information for creating SQL command file."""
        if genNewSw:
            import re
            r = re.compile( '\w+' )
            if r.match( tableName ):
                self.fd.write( 
                  sqltemplate.dataHdr % 
                  (tableName, tableName, tableName, tableName) 
                  )
            else:
                raise AttributeError( 'Invalid table name' )
        
    def write( self, metricName, srcFileName, varName, value ):
        """ Generate the Sql INSERT line into the sql command file."""
        self.datanum += 1
        #
        sArgs = ','.join( (
            self.IDDateTime,
            str( self.datanum ),
            '"'+str( self.libName )+'"',
            '"'+str( metricName )+'"',
            '"'+str( srcFileName )+'"',
            '"'+str( varName )+'"',
            '"'+str( value )+'"'
            ) )
        sOut = sqltemplate.dataInsert % (self.tableName, sArgs)
        self.fd and self.fd.write( sOut )

    def close( self ):
        """ Close file, if it is opened."""
        self.fd and self.fd.close()
        self.fd = None
