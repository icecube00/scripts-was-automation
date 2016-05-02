@echo off
@cd /d "%~dp0"

chcp 1251>NUL

if not defined scriptLoc (
 for %%I in ("%~dp0.") do set scriptLoc=%%~fI
)

for /f "tokens=1-4 delims=. " %%a in ('echo %DATE:/=.%') do (
 if [%%d]==[] (
  if not defined mydate set mydate=%%c-%%b-%%a
  set RegSettings=True
 ) else (
  if not defined mydate set mydate=%%d-%%b-%%c
  set RegSettings=False
 )
)
for /f "tokens=1-3 delims=/:, " %%a in ('echo %time%') do (
 if not defined mytime set mytime=%%a-%%b-%%c
)

pushd..
 set UTIL_DIR=%CD%\util
popd

if not defined SCRIPT_DIR_NAME set SCRIPT_DIR_NAME=%scriptLoc%\py
set LOG_DIR=%UTIL_DIR%\log
set CONFIG_DIR_NAME=%UTIL_DIR%\_stop_server
set LOG_FILE=%mydate%_%mytime%_cluster_stop.log

set /a counter=0
if not defined DMGR_HOME call:checkenvconf
if not defined DMGR_HOME call:check_define

if defined %USER_LOGIN% set userParams=-username %USER_LOGIN% -password %USER_PASSWORD%

if exist %DMGR_HOME%\bin\serverStatus.bat (
 call %DMGR_HOME%\bin\serverStatus.bat -all -profileName %DMGR_PROFILE% %userParams%|find "STARTED" && goto:stopDMGR
) else (
 call:SCRIPTEND "[Ошибка] Не найден файл консоли IBM WebSphere: %DMGR_HOME%\bin\serverStatus.bat" exit
)
goto:clearTEMP

:stopDMGR
call:writetolog "Выполняем полную остановку кластера"
if exist %DMGR_HOME%\bin\wsadmin.bat (
 "%DMGR_HOME%\bin\wsadmin.bat" -lang jython %ENVPROPS% %userParams% -f .\py\create_env.py
) else (
 call:SCRIPTEND "[Ошибка] Не найден файл управления консолью IBM WebSphere: %DMGR_HOME%\bin\wsadmin.bat" exit
)

:clearTEMP
 call:writetolog "Удаляем временные файлы менджера развёртывания - DMGR"
 del %DMGR_HOME%\wstemp\* /s /q
 del %DMGR_HOME%\temp\* /s /q
 del %DMGR_HOME%\tranlog\* /s /q
 del %DMGR_HOME%\javacore.*.txt /s /q

 call:writetolog "Удаляем временные агентов узлов."
 del %NODE_AGENT_HOME%\wstemp\* /s /q
 del %NODE_AGENT_HOME%\temp\* /s /q
 del %NODE_AGENT_HOME%\tranlog\* /s /q
 del %NODE_AGENT_HOME%\javacore.*.txt
 del %NODE_AGENT_HOME%\logs\syncNode.log /s /q
)
call:SCRIPTEND "Результат работы скрипта записан в %LOG_DIR%\%LOG_FILE%" exit
goto:EOF

:checkenvconf
if exist %UTIL_DIR%\envconf.bat (
 pushd %UTIL_DIR%\
 call %UTIL_DIR%\envconf.bat 
 popd
) else (
 set ENVPROPS=
 set SUFFIX=""
)
goto:EOF

:check_define
if NOT DEFINED DMGR_HOME ( 
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
 call:writetolog "%counter% раза неправильно введен параметр директории менеджера развертывания Dmgr IBM WebSphere"
 goto:EOF
)
goto:EOF

:check_null
if "%DMGR_HOME%"=="" (
 call:writetolog "Вы не указали путь до директории менеджера развертывания Dmgr IBM WebSphere!"
 goto:check_define
) else (
 call:writetolog "В качестве директории менеджера развертывания Dmgr IBM WebSphere Вы указали: %DMGR_HOME%"
)
goto:EOF

:SCRIPTEND
call:writetolog "%~1"
call:writetolog "Результат работы скрипта записан в %LOG_DIR%\%LOG_FILE%"
call:writetolog "Работа скрипта остановки кластера завершена"
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
