@echo off
@echo --- authority
pause

set QMGR=M00.SIRIUS

rem Sirius User
set AUTHUSER=srs99usr
rem CHANNEL(SC.SIRIUS)
setmqaut -m %QMGR% -p %AUTHUSER% -t qmgr +connect +inq
setmqaut -m %QMGR% -p %AUTHUSER% -t q -n Q.SIRIUS.AUDIT +get +put +inq +browse
setmqaut -m %QMGR% -p %AUTHUSER% -t q -n Q.SIRIUS.DATA.ERIB +get +put +inq +browse
setmqaut -m %QMGR% -p %AUTHUSER% -t q -n Q.SIRIUS.ICON.ERIB +get +put +inq +browse
setmqaut -m %QMGR% -p %AUTHUSER% -t q -n Q.SIRIUS.LOG +get +put +inq +browse
setmqaut -m %QMGR% -p %AUTHUSER% -t q -n Q.SIRIUS.TEMP +get +put +inq +browse
setmqaut -m %QMGR% -p %AUTHUSER% -t q -n Q.SIRIUS.TO.SVISTA +get +put +inq +browse
setmqaut -m %QMGR% -p %AUTHUSER% -t q -n Q.SVISTA.TO.SIRIUS +get +put +inq +browse
rem SmartVista User
set AUTHUSER=sv99usr
rem CHANNEL(SC.SVISTA)
setmqaut -m %QMGR% -p %AUTHUSER% -t qmgr +connect +inq
setmqaut -m %QMGR% -p %AUTHUSER% r -t q -n Q.SIRIUS.TO.SVISTA +get +inq +browse
setmqaut -m %QMGR% -p %AUTHUSER% r -t q -n Q.SVISTA.TO.SIRIUS +put +inq +browse
@echo --------------------------------- Authority: ended
