@echo off
For /f "tokens=1-4 delims=/. " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
For /f "tokens=1-2 delims=/: " %%a in ('time /t') do (set mytime=%%a-%%b)
@echo --- update TIMESTAMP is: %mydate%_%mytime%
pause
set UPVER=4050
set QMGR=M00.SIRIUS
@echo --- Queue Manager is: %QMGR%
runmqsc %QMGR% < update_%QMGR%_%UPVER%.mqsc >> report_%QMGR%_%mydate%_%mytime%.txt
call update_%QMGR%_%UPVER%_auth.bat