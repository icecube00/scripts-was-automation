@echo off

@cd /d "%~dp0"

chcp 1251 > NUL

if not defined scriptLoc (
 set scriptLoc=%CD%
)
for /f "tokens=1-4 delims=. " %%a in ('echo %DATE:/=.%') do (
 if [%%d]==[] (
  set mydate=%%c-%%b-%%a
  set RegSettings=True
 ) else (
  set mydate=%%d-%%b-%%c
  set RegSettings=False
 )
)
for /f "tokens=1-3 delims=/:, " %%a in ('echo %time%') do (
 set mytime=%%a-%%b-%%c
)

pushd..
 set UTIL_DIR=%CD%\util
 set WAS_DIR=%CD%\WAS
popd

if not defined LOG_DIR set LOG_DIR=%WAS_DIR%\logs
if not defined SCRIPT_DIR_NAME set SCRIPT_DIR_NAME=%WAS_DIR%\py
set LOG_FILE=%mydate%_%mytime: =0%_sirius_configuration_log.log
set CONFIG_DIR_NAME=%UTIL_DIR%\_install


if exist %UTIL_DIR%\envconf.bat (
 pushd %UTIL_DIR%\
 call %UTIL_DIR%\envconf.bat 
 popd
) else (
 set ENVPROPS=
 set SUFFIX=""
)

call:writetolog "Запуск скрипта подготовки WebSphere"
set /a counter=0

:check_define
if not defined DMGR_HOME ( 
 call:writetolog "Переменная DMGR_HOME не определена."
 goto:SET_DMGR_HOME
) else (
 call:writetolog "Переменная DMGR_HOME определена."
 goto:check_null
)
goto:EOF

:SET_DMGR_HOME
if %counter% leq 2 (
 set /a counter=counter+1
 chcp 866 > NUL
 set /P DMGR_HOME="Пожалуйста, укажите полный путь до директории менеджера развертывания Dmgr IBM WebSphere: " 
 chcp 1251 > NUL
 goto:check_null
) else (
 call:SCRIPTEND "[Ошибка] %counter% раза неправильно введен параметр директории менеджера развертывания Dmgr IBM WebSphere" exit
)
goto:EOF

:check_null
if "%DMGR_HOME%"=="" (
 call:writetolog "Вы не указали путь до директории менеджера развертывания Dmgr IBM WebSphere!"
 goto:check_define
) else (
 call:writetolog "В качестве директории менеджера развертывания Dmgr IBM WebSphere Вы указали: %DMGR_HOME%"
 goto:exec_wsadm
)
goto:EOF

:exec_wsadm
if defined USER_LOGIN set userParams=-username %USER_LOGIN% -password %USER_PASSWORD%
set WS=%WAS_DIR%
set APP_WS=%WAS_DIR%\dist
if exist %DMGR_HOME%\bin\wsadmin.bat (
 "%DMGR_HOME%\bin\wsadmin.bat" -lang jython %ENVPROPS% %userParams% -f .\py\create_env.py
) else (
 call:SCRIPTEND "[Ошибка] Не найден файл управления консолью IBM WebSphere: %DMGR_HOME%\bin\wsadmin.bat" exit
)
goto:EOF

:SCRIPTEND
call:writetolog "%~1"
call:writetolog "Результат работы скрипта записан в %LOG_DIR%\%LOG_FILE%"
call:writetolog "Работа скрипта развертывания АС СИРИУС завершена"
if "%~2"=="exit" (
 @echo Ќ ¦¬ЁвҐ «оЎго Є« ўЁиг, зв®Ўл Їа®¤®«¦Ёвм... > CON
 pause>NUL
 exit
)
goto:EOF

:writetolog
 set logdata=%~1
 @echo %logdata% >>%LOG_DIR%\%LOG_FILE%
 chcp 866>NUL
 chcp 866>NUL
 @echo %Date% %Time% %logdata% > CON
 chcp 1251>NUL
goto:EOF
