'''
Created on Jan 28 2014
Last Update 2015 01 14
@author: sbt-orlov-pa 
@modified by: sbt-al-gurabi-ia
'''
##########################
DB_INSTALL_TYPE="new"
##########################
XA_TRANSACTION="FALSE"
##########################
CLEAR_CACHE="TRUE"
##########################
STOP_SERVER="TRUE"
##########################
CONFIG_WAS="TRUE"
##########################
INSTALL_APPS="TRUE"
##########################
SIRIUS_DB_BUSINESS_HOST=""
SIRIUS_DB_BUSINESS_PORT="1521"
SIRIUS_DB_BUSINESS_NAME=""
SIRIUS_DB_BUSINESS_LOGIN=""
SIRIUS_DB_BUSINESS_PASSW=""
##########################
SIRIUS_LOG_DB_HOST=""
SIRIUS_LOG_DB_PORT="1521"
SIRIUS_LOG_DB_NAME=""
SIRIUS_LOG_DB_LOGIN="semisystem"
SIRIUS_LOG_DB_PASSW="s"
##########################
SIRIUS_LOG_DB_ARCH_HOST=""
SIRIUS_LOG_DB_ARCH_PORT="1521"
SIRIUS_LOG_DB_ARCH_NAME=""
##########################
SIRIUS_DB_MERCH_HOST=""
SIRIUS_DB_MERCH_PORT="1521"
SIRIUS_DB_MERCH_NAME=""
SIRIUS_DB_MERCH_LOGIN=""
SIRIUS_DB_MERCH_PASSW=""
MERCH_DB_TABLE=""
##########################
SIRIUS_DB_USER="SIRIUS5"
SIRIUS_DB_PASSWORD_CLIENT=""
SIRIUS_USER_NEW_PASSW=""
##########################
SIRIUS_SETTINGS_DB_USER="SIRIUS_CFG"
SIRIUS_SETTINGS_DB_PASSWORD_CLIENT=""
##########################
SIRIUS_CACHE_DB_USER="SIRIUS_CACHE"
SIRIUS_CACHE_DB_PASSWORD_CLIENT=""
##########################
SIRIUS_LOG_DB_USER="SIRIUS_LOG5"
SIRIUS_LOG_DB_PASSWORD_CLIENT=""
##########################
SIRIUS_LOG_DB_ARCH_USER="SIRIUS_LOG5"
SIRIUS_LOG_DB_ARCH_PASSWORD_CLIENT=""
##########################
SIRIUS_ERIB_DB_USER="SIRIUS_ERIB"
SIRIUS_ERIB_DB_PASSWORD_CLIENT=""
##########################
SIRIUS_USER_OLD="SIRIUS5"
SIRIUS_USER_UTIL="SIRIUS_UTIL"
SIRIUS_USER_TIVOLI="SIRIUS_TIVOLI"
##########################
SIRIUS_BASIC_ROLE="SIRIUS_BASIC_ROLE"
SIRIUS_WAS_CLIENT_ROLE="SIRIUS_WAS_CLIENT_ROLE"
SIRIUS_TIVOLI_ROLE="SIRIUS_TIVOLI_ROLE"
##########################
MQ_HOST=""
MQ_PORT="3333"
MQ_MANAGER="M00.SIRIUS"
MQ_SSL_CONF="MQSSL"
##########################
MQ_HOST_LOG=""
MQ_PORT_LOG="3333"
MQ_MANAGER_LOG="M00.SIRIUS"
##########################
SIRIUS_LIBS="${WAS_INSTALL_ROOT}/lib/ext"
SYSTEM_LIBS="${WAS_INSTALL_ROOT}/lib/ext"
##########################
APP_TO_UNINSTALL="SiriusVistaReader.ear,SiriusLogger.ear,Sirius.ear,Arm.ear,sirius-journal-writer.ear"
APP_TO_INSTALL="sirius-vista-reader.ear,sirius-server.ear,sirius-journal-old-writer.ear,sirius-journal-writer.ear,sirius-arm-server.ear,sirius-arm-settings.war,sirius-arm-monitoring.war,sirius-arm-claim.war,sirius-arm-audit.war,sirius-fault-notifier.war"
##########################

##########################
CONFIG_SSL="TRUE"
##########################
HTTPS_ERIB_Cert="erib-client.ca.sbrf.ru"
MQSSL_ClientKey="00ca0001csiriussrs99usr"
MQSSL_ServerKey="00ca0001csiriussrs99usr"
HTTPS_ClientKey="erib-client.ca.sbrf.ru"
HTTPS_ServerKey="sirius_multserver"
##########################
#SSL_CERTIFICATES_FOLDER=""
############SIGNERS CERTIFICATE FILES##############
#sberbank_enterprise_ca_2021="sberbank_enterprise_ca_2021.cer"
#sberbank_root_ca_2021="sberbank_root_ca_2021.cer"
#erib_datapower="erib_datapower.cer"
#intermediate_pem1="intermediate_pem1.cer"
#intermediate_pem2="intermediate_pem2.cer"
#root_pem="root_pem.cer"
############SIGNERS CERTIFICATE FILES##############
#SSL_MQSSL_PASS = "GENERATE"
#SSL_MQSSL_SELFSTORE = "sirius.jks"
#SSL_MQSSL_SELFSTORE_PASS = "123456"
#SSL_MQSSL_SELFSTORE_TYPE = "JKS"
##########################
#SSL_HTTPS_PASS = "GENERATE"
#SSL_HTTPS_SELFSTORE = "sirius.jks"
#SSL_HTTPS_SELFSTORE_PASS = "123456"
#SSL_HTTPS_SELFSTORE_TYPE = "JKS"
##########################

##########################
SET_TRACE_LEVEL = 'TRUE'
SET_NEW_TRACE = {'*':'detail','oracle.jdbc.*':'all'}
KEEP_TRACE_CONF = 'FALSE'
##########################