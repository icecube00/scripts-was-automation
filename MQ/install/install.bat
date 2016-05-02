@echo off
set QMGR=M00.SIRIUS

echo ************ %QMGR% **********
@echo --- install
pause

set LOG_FILE_SIZE=16384
set LOG_PRIMARY_FILES=8
set LOG_SECONDARY_FILES=4

set DEADQ=Q.SIRIUS.DLQ
set MAXCHANNELS=1000
set CLIENTIDLE=3600
set KeepAlive=YES

endmqm -i %QMGR%
endmqlsr -m %QMGR%

rem dltmqm %QMGR%

crtmqm -lf %LOG_FILE_SIZE% -lp %LOG_PRIMARY_FILES% -ls %LOG_SECONDARY_FILES% -u %DEADQ% %QMGR%

amqmdain manual %QMGR%
amqmdain reg %QMGR% -c add -s Channels -v MaxChannels=%MAXCHANNELS%
rem amqmdain reg %QMGR% -c add -s Channels -v ClientIdle=%CLIENTIDLE%
amqmdain reg %QMGR% -c add -s SSL -v OCSPAuthentication=OPTIONAL
rem amqmdain reg %QMGR% -c add -s TCP -v KeepAlive=%KeepAlive%

amqmdain start %QMGR%
call createq.bat
call updatesyschlssl.bat
call authority.bat
amqmdain end %QMGR%

rem ���� ��� ���������� �������� MSCS
@echo hamvmqm QMgr '%QMGR%'
rem hamvmqm /m %QMGR% /dd "k:\IBM\WebSphere MQ" /ld "k:\IBM\WebSphere MQ\log"