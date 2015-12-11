#!/bin/sh

# this will get better later

LIBFILES="Exceptions.py Options.py"

BINFILES="
CopyData
DbDebugger
DescribeObject
DescribeSchema
DumpCSV
DumpData
ExportColumn
ExportData
ExportObjects
ExportXML
GeneratePatch
GenerateView
ImportColumn
ImportData
ImportXML
PatchDB
RebuildTable
RecompileSource
"

LIBDIR=/usr/local/sqlminus/lib/python2.7/site-packages
BINDIR=/usr/local/sqlminus/bin

cp $LIBFILES $LIBDIR
cp $BINFILES $BINDIR
