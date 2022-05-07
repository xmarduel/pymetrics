""" Compute HalsteadMetric Metrics. 

HalsteadMetric metrics, created by Maurice H. HalsteadMetric in 1977, consist 
of a number of measures, including:

Program length (N):     N = N1 + N2
Program vocabulary (n): n = n1 + n2
Volume (V):             V = N * LOG2(n)
Difficulty (D):         D = (n1/2) * (N2/n2)
Effort (E):             E = D * V
Average Volume (avgV)   avgV = sum(V)/m
Average Effort (avgE)   avgE = sum(E)/m

where:

n1 = number of distinct operands
n2 = number of distinct operators
N1 = total number of operands
N2 = total number of operators
m  = number of modules

What constitues an operand or operator is often open to 
interpretation. In this implementation for the Python language:

    operators are of type OP, INDENT, DEDENT, or NEWLINE since these
        serve the same purpose as braces and semicolon in C/C++, etc.
    operands are not operators or whitespace or comments 
        (this means operands include keywords)

    $Id: halstead.py,v 1.5 2009/10/30 18:39:13 xavier Exp $
"""
__version__ = "$Revision: 1.5 $"[11:-2]
__author__ = 'Reg. Charney <pymetrics@charneyday.com>'

import os
import math
import time
from metricbase import MetricBase
from globals import *

class HalsteadMetric( MetricBase ):
    """ Compute various HalsteadMetric metrics. """
    totalV = 0
    totalE = 0
    numModules = 0
    def __init__( self, context, runMetrics, metrics, pa, *args, **kwds ):
        """ Initialization for the HalsteadMetric metrics."""
        self.inFile = context['inFile']
        self.context = context
        self.runMetrics = runMetrics
        self.metrics = metrics
        self.pa = pa
        self.inFile = context['inFile']
        self.numOperators = 0
        self.numOperands = 0
        self.uniqueOperators = {}
        self.uniqueOperands = {}
        HalsteadMetric.numModules += 1
        
        # initialize category accummulators as dictionaries
        self.hsDict = {}
        for t in ['token','stmt','block','function','class','module','run']:
            self.uniqueOperators[t] = {}
            self.uniqueOperands[t] = {}
            #for v in ['N','N1','N2','n','n1','n2','V','D','E','avgV','avgE']:
            #    self.hsDict[(t,v)] = 0
        
    def processToken( self, currentFcn, currentClass, tok, *args, **kwds ):
        """ Collect token data for Halstead metrics."""
        if tok.type in [WS, EMPTY, ENDMARKER, NEWLINE, EMPTY, COMMENT]:
            pass
        elif tok.type in [OP, INDENT, DEDENT]:
            self.numOperators += 1
            self.uniqueOperators['token'][tok.text] = self.uniqueOperators['token'].get(tok.text, 0) + 1
        else:
            self.numOperands += 1
            sDict = self.context.__repr__()
            k = (sDict,tok.text)
            self.uniqueOperands['token'][k] = self.uniqueOperands['token'].get(tok.text, 0) + 1

    def processStmt( self, currentFcn, currentClass, stmt, *args, **kwds ):
        """ Collect statement data for Halstead metrics."""
        
        result = None
        
        # the two lines following this comment would compute the Halstead 
        # metrics for each statement in the run, However, it is 
        # normally overkill, so these lines are commented out.
        
        #lineNum = stmt[0].row
        #result = self.computeCategory( 'stmt', lineNum, stmt )
        
        return result
        
    def processBlock( self, currentFcn, currentClass, block, *args, **kwds ):
        """ Collect block data for Halstead metrics."""

        result = None

        # the two lines following this comment would compute the Halstead 
        # metrics for each statement in the run, However, it is 
        # normally overkill, so the two lines are commented out.
        
        #blockNum = self.context['blockNum']
        #result = self.computeCategory( 'block', blockNum, block )
        
        return result

    def processFunction( self, currentFcn, currentClass, fcn, *args, **kwds ):
        """ Collect function data for Halstead metrics."""
        result = self.computeCategory( 'function', currentFcn, fcn )
        return result
        
    def processClass( self, currentFcn, currentClass, cls, *args, **kwds ):
        """ Collect class data for Halstead metrics."""
        if currentClass :
            result = self.computeCategory( 'class', currentClass, cls )
            return result
        else:
            return self.hsDict
        
    def processModule( self, moduleName, mod, *args, **kwds ):
        """ Collect module data for Halstead metrics."""
        result = self.computeCategory( 'module', moduleName, mod )
        return result
        
    def processRun( self, run, *args, **kwds ):
        """ Collect run data for Halstead metrics."""
        datestamp = time.strftime("%Y-%m-%d.%H:%m%Z",time.localtime())
        #result = self.computeCategory( 'run', datestamp, run )
        #return result
        return self.hsDict
        
    def __LOGb( self, x, b ): 
        """ convert to LOGb(x) from natural logs."""
        try:
            result = math.log( x ) / math.log ( b )
        except OverflowError:
            result = 1.0
        return result

    def computeIncr( self, cat, tok, uniqueOperators, uniqueOperands ):
        """ Compute increment for token depending on which category it falls into."""
        operatorIncr = operandIncr = 0
        if tok.type in [WS, EMPTY, ENDMARKER, NEWLINE, EMPTY, COMMENT]:
            return (operatorIncr,operandIncr)
            
        if tok.type in [OP, INDENT, DEDENT]:
            operatorIncr = 1
            uniqueOperators[tok.text] = uniqueOperators.get(tok.text, 0) + 1
        else:
            operandIncr = 1
            uniqueOperands[tok.text] = uniqueOperands.get(tok.text,0) + 1
            
        return (operatorIncr,operandIncr)
        
    def computeCategory( self, cat, mod, lst ):
        """ Collection data for cat of code."""
        numOperators = numOperands = 0
        for tok in lst:
            result = self.computeIncr( cat, tok, self.uniqueOperators[cat], self.uniqueOperands[cat] )
            numOperators += result[0]
            numOperands += result[1]
        result = self.compute( cat, mod, numOperators, numOperands, self.uniqueOperators[cat], self.uniqueOperands[cat] )
        return result
        
    def compute( self, cat, mod, numOperators, numOperands, uniqueOperators, uniqueOperands, *args, **kwds ):
        """ Do actual calculations here."""
        
        modID= id( mod )
        #
        n1 = len( uniqueOperands )
        n2 = len( uniqueOperators )
        N1 = numOperands
        N2 = numOperators
        N = N1 + N2
        n = n1 + n2
        V = float(N) * self.__LOGb( n, 2 )
        try:
            D = (float(n1)/2.0) * (float(N2)/float(n2))
        except ZeroDivisionError:
            D = 0.0
        E = D * V
        HalsteadMetric.totalV += V
        HalsteadMetric.totalE += E
        avgV = HalsteadMetric.totalV / HalsteadMetric.numModules
        avgE = HalsteadMetric.totalE / HalsteadMetric.numModules
        
        self.hsDict[(cat,modID)] = {}
        self.hsDict[(cat,modID)]['n1'] = n1
        self.hsDict[(cat,modID)]['n2'] = n2
        self.hsDict[(cat,modID)]['N1'] = N1
        self.hsDict[(cat,modID)]['N2'] = N2
        self.hsDict[(cat,modID)]['N'] = N
        self.hsDict[(cat,modID)]['n'] = n
        self.hsDict[(cat,modID)]['V'] = V
        self.hsDict[(cat,modID)]['D'] = D
        self.hsDict[(cat,modID)]['E'] = E
        self.hsDict[(cat,modID)]['numModules'] = HalsteadMetric.numModules
        self.hsDict[(cat,modID)]['avgV'] = avgV
        self.hsDict[(cat,modID)]['avgE'] = avgE

        self.hsDict[(cat,modID)]['cat'] = {'module':'(M)', 'class':'(C)', 'function':'(F)'}[cat]
        self.hsDict[(cat,modID)]['mod'] = mod
        
        return self.hsDict
        
    def display( self, cat=None ):
        """ Display the computed Halstead Metrics."""
        if self.pa.quietSw:
            return self.hsDict
            
        hdr = "\nHalstead Metrics for %s" % self.inFile
        print hdr
        print "-"*len(hdr) + '\n'
        
        if len( self.hsDict ) == 0:
            print "%-8s %-30s " % ('**N/A**','All Halstead metrics are zero')
            return self.hsDict

        hdr1 = "Cat Identifier                                         D         E              N     N1     N2 V         avgE      avgV          n    n1  n2"
        hdr2 = "--- -------------------------------------------------- --------- --------- ------ ------ ------ --------- --------- --------- ----- ----- ---"
        #       123 12345678901234567890123456789012345678901234567890 123456789 123456789 123456 123456 123456 123456789 123456789 123456789 12345 12345 123
        fmt = "%(cat)-3s %(mod)-50.50s %(D)9.2e %(E)9.2e %(N)6d %(N1)6d %(N2)6d %(V)9.2e %(avgE)9.2e %(avgV)9.2e %(n)5d %(n1)5d %(n2)3d"

        print hdr1
        print hdr2
        
        keys = self.hsDict.keys()
        #
        def cmp_by_name(x,y):
            if   self.hsDict[x]['mod'] < self.hsDict[y]['mod'] : return -1
            elif self.hsDict[x]['mod'] > self.hsDict[y]['mod'] : return  1
            else : return 0
        #
        def keysort(x,y):
            '''
            level = '1' if module            
            level = '1-k' k>0 if class module
            level = '1-0-n' if function
            level = '1-k-n' if method (k>0)
            '''
            level_x = self.hsDict[x]['level']
            level_y = self.hsDict[y]['level']
            #
            level_x_list = level_x.split("-")
            level_y_list = level_y.split("-")
            #
            for mx,my in zip(level_x_list, level_y_list):
                if mx < my : return -1
                if mx > my : return 1
                if mx == my : pass
            if len(level_x_list) < len(level_y_list):
                return -1
            else:
                return 1
        #
        module_keys = filter(lambda x:self.hsDict[x]['cat'] == '(M)',  keys)
        class_keys = filter(lambda x:self.hsDict[x]['cat'] == '(C)',  keys)
        function_keys = filter(lambda x:self.hsDict[x]['cat'] == '(F)',  keys)
        #
        module_keys.sort(cmp=cmp_by_name)
        #for key in module_keys: print self.hsDict[key]['mod']
        class_keys.sort(cmp=cmp_by_name)
        #for key in class_keys: print self.hsDict[key]['mod']
        function_keys.sort(cmp=cmp_by_name)
        #for key in function_keys: print self.hsDict[key]['mod']
        #
        classlist = [ self.hsDict[kkey]['mod'] for kkey in class_keys ]
        #
        for k, key in enumerate(module_keys):
            self.hsDict[key]['level'] = "%d" % (k+1)
        for k, key in enumerate(class_keys):
            self.hsDict[key]['level'] = "1-%d" % (k+1)
        for k, key in enumerate(function_keys):
            if "." in self.hsDict[key]['mod']:
                class_owner = self.hsDict[key]['mod'].split(".")[0]
                k1 = classlist.index(class_owner)
            else:
                k1 = -1
            #
            self.hsDict[key]['level'] = "1-%d-%d" % (k1+1,k+1)
        #   
        keys.sort(cmp=keysort)
        
        for key in keys:
            self.fix_mod_name(key)
            #
            print fmt % self.hsDict[key]
            
        print ""
            
        code = '''Program length (N):     N = N1 + N2
Program vocabulary (n): n = n1 + n2
Volume (V):             V = N * LOG2(n)
Difficulty (D):         D = (n1/2) * (N2/n2)
Effort (E):             E = D * V
Average Volume (avgV)   avgV = sum(V)/m
Average Effort (avgE)   avgE = sum(E)/m

where:

n1 = number of distinct operands
n2 = number of distinct operators
N1 = total number of operands
N2 = total number of operators
m  = number of modules'''

        print code    
        return self.hsDict

    def fix_mod_name(self, key):
        '''
        '''
        mod = self.hsDict[key]['mod']
        #
        if len(mod) > 50:
            if "\\" in mod:
                moddir, modname = os.path.split(mod)
                mod = moddir[:50-3-1-len(modname)] + "..." + "\\" + modname 
                self.hsDict[key]['mod'] = mod
            elif "." in mod:
                idx1 = 25
                idx2 = - 50 + 3 + idx1 + len(mod)
                # idx1 + 3 + (len-idx2) = 50
                mod = mod[:idx1] + "..." + mod[idx2:] 
                self.hsDict[key]['mod'] = mod
            else:
                idx1 = 25
                idx2 = - 50 + 3 + idx1 + len(mod) 
                # idx1 + 3 + (len-idx2) = 50
                mod = mod[:idx1] + "..." + mod[idx2:] 
                self.hsDict[key]['mod'] = mod