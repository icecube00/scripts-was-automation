@echo off
@echo --- updatesyschlsl
pause

set QMGR=M00.SIRIUS
runmqsc %QMGR% < updatesyschlssl.mqsc >> report_%QMGR%.txt
