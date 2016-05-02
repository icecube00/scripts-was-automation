@echo off
@echo --- Authority TIMESTAMP is: %mydate%_%mytime%
pause

set QMGR=M00.SIRIUS
rem Sirius User
set AUTHUSER=srs99usr
setmqaut -m %QMGR% -p %AUTHUSER% -t q -n Q.SIRIUS.TO.SVISTA +get +put +inq +browse >> report_%QMGR%_%mydate%_%mytime%.txt

rem SmartVista User
set AUTHUSER=sv99usr
rem CHANNEL(SC.SVISTA)
setmqaut -m %QMGR% -p %AUTHUSER% r -t q -n Q.SIRIUS.TO.SVISTA +get +inq +browse >> report_%QMGR%_%mydate%_%mytime%.txt
@echo --------------------------------- Authority: ended