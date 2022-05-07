""" sqltemplate - template for generating sql token output. """

__revision__ = "$Revision: 1.2 $"[11:-2]
__author__ = 'Reg. Charney <pymetrics@charneyday.com>'


tokenHdr = """--
-- Automatically generated table structure for token table `%s`
--

DROP TABLE IF EXISTS "%s";

CREATE TABLE "%s" (
  "IDDateTime" datetime NOT NULL default '0000-00-00 00:00:00',
  "ID" integer unsigned NOT NULL,
  "libraryName" varchar(32) default '',
  "fileName" varchar(255) default NULL,
  "lineNum" integer NOT NULL,
  "colNum" integer NOT NULL,
  "type" varchar(16) NOT NULL default 'ERRORTOKEN',
  "semtype" varchar(16) default NULL,
  "textLen" integer NOT NULL default 1,
  "text" varchar(255) NOT NULL default '',
  "fqnFunction" varchar(255) default NULL,
  "fqnClass" varchar(255) default NULL,
  "blockNum" integer NOT NULL default 1,
  "blockDepth" integer NOT NULL default 0,
  "fcnDepth" integer NOT NULL default 0,
  "classDepth" integer NOT NULL default 0,
  "parenDepth" integer NOT NULL default 0,
  "bracketDepth" integer NOT NULL default 0,
  "braceDepth" integer NOT NULL default 0,
  PRIMARY KEY (ID,fileName)
);

--
-- Load data for table `%s`
--
"""


tokenInsert = """INSERT INTO %s VALUES (%s);\n"""

dataHdr = """
-- Automatically generated table structure for metric data table `%s`
--

DROP TABLE IF EXISTS "%s";

CREATE TABLE "%s" (
  "IDDateTime" datetime NOT NULL default '0000-00-00 00:00:00',
  "ID" integer unsigned NOT NULL,
  "libraryName" varchar(32) default '',
  "metricName" varchar(32) NOT NULL default '',
  "srcFileName" varchar(255) NOT NULL default '',
  "varName" varchar(255) NOT NULL default '',
  "value" decimal NOT NULL default '0',
  PRIMARY KEY (ID, srcFileName)
);


--
-- Load metric data for table `%s`
--
"""

dataInsert = """INSERT INTO %s VALUES (%s);\n"""

