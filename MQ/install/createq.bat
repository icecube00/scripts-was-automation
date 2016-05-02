@echo off
@echo --- createq
pause

set QMGR=M00.SIRIUS
runmqsc %QMGR% < %QMGR%.mqsc >> report_%QMGR%.txt
