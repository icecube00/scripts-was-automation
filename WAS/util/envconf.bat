:: Uncomment following lines and set the login and password 
:: for WAS user with rights for deployment manager

::set USER_LOGIN=wasadmin
::set USER_PASSWORD=wasadmin

set WAS_PROFILES=D:\IBM\AppServer_Sirius\profiles
set APP_SRV_ROOT=D:\IBM\AppServer_Sirius

set DMGR_PROFILE=Dmgr01
set NODE_AGENT_PROFILE=AppSrv01

set DMGR_HOME=%WAS_PROFILES%\%DMGR_PROFILE%
set NODE_AGENT_HOME=%WAS_PROFILES%\%NODE_AGENT_PROFILE%
