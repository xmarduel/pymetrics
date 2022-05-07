""" MyToken - PyMetrics' version of Token. 

    $Id: mytoken.py,v 1.1.1.1 2009/10/10 08:22:31 xavier Exp $
"""
__version__ = "$Revision: 1.1.1.1 $"[11:-2]
__author__ = 'Reg. Charney <pymetrics@charneyday.com>'

import token
from PyMetrics.globals import *

class MyToken:
    def __init__(self, **kwds ):
        """ Initialize class with user-defined keywords."""
        self.__dict__.update(kwds)

    def __repr__( self ):
        """ Pretty print token. 
        
        Don't print text for special token types since they do not have 
        useful visible representation, other than blank. 
        """
        tn = token.tok_name[self.type]        
        sn = self.semtype
        if sn:
            sn = token.tok_name[self.semtype]
        if self.type in [WS,NEWLINE,INDENT,DEDENT,EMPTY,ENDMARKER]:
            s = "[type=%s semtype=%s row=%s col=%s len=%d]" % (tn,sn,self.row,self.col,len(self.text))
        else:
            if self.type == COMMENT and self.text[-1] == '\n':
                self.text = self.text[:-1]
            s = "[type=%s semtype=%s row=%s col=%s len=%d text=<%s>]" % (tn,sn,self.row,self.col,len(self.text),self.text)
        return s

