@echo off
@echo --- Authority TIMESTAMP is: %mydate%_%mytime%
pause

set QMGR=M00.SIRIUS
set AUTHUSER=srs99usr
setmqaut -m %QMGR% -p %AUTHUSER% -t q -n Q.SIRIUS.AUDIT +put +get +browse +inq >> report_%QMGR%_%mydate%_%mytime%.txt