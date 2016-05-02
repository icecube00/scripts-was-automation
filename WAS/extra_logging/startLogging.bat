echo off

rem required parameters
set WSADMIN=
set APP_SERVER_NAME=


rem check attribute
if "%1"=="/?" (
    goto help
)
if "%WSADMIN%"=="" (
    if "%1"=="" (
        set /p WSADMIN="Enter path to wsadmin.bat: "
    )
)
if "%APP_SERVER_NAME%"=="" (
    if "%2"=="" (
        set /p APP_SERVER_NAME="Enter name of application server: "
    )
)

rem get path to directory from file and delete this file
call %WSADMIN% -lang jython -f "get_log4j_conf_dir.py" --server=%APP_SERVER_NAME%
if exist _.temp (
    set /p LOG4J_CONF_DIR=<_.temp
    del _.temp
)
rem check to get directory from WAS
echo "%LOG4J_CONF_DIR%"
if "%LOG4J_CONF_DIR%"=="" (
    goto failure1
)
rem copy log4j properties to target directory
copy /y log4j\log4j2-sirius*.xml %LOG4J_CONF_DIR%
goto end

:error
echo The syntax of the command is incorrect

:help
echo.
echo Usage: startLogging.bat wsadmin serverName
echo.
echo script options:
echo     wsadmin       - Path to wsadmin.bat
echo     serverName    - The name of the application server to which the command applies
goto end

:failure1
echo Failure: Could not find the target directory
goto end

:end