'''
Last Update 2016 02 20

@author: sbt-orlov-pa
@modified by: sbt-al-gurabi-ia

'''
from config import *
from system import *
from log import log2file
from log import curTime    

try:
    sufFix = java.lang.System.getenv('SUFFIX')
    if sufFix!=None:
        sufFix = sufFix.replace('\"','')
    #end if
    else:
        sufFix=''
    #end else
    SIRIUS_DB_RENEW = "TRUE"
    descDateTime = curTime("now")
    sharedLibsArray = [{"SiriusSL": [
                                      "${SIRIUS_LIB_PATH}/asm-3.3.1.jar",
                                      "${SIRIUS_LIB_PATH}/jackson-core-asl-1.9.13.jar",
                                      "${SIRIUS_LIB_PATH}/jackson-jaxrs-1.9.13.jar",
                                      "${SIRIUS_LIB_PATH}/jackson-mapper-asl-1.9.13.jar",
                                      "${SIRIUS_LIB_PATH}/jackson-xc-1.9.13.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-client-1.18.1.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-core-1.18.1.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-json-1.18.1.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-multipart-1.18.1.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-server-1.18.1.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-servlet-1.18.1.jar",
                                      "${SIRIUS_LIB_PATH}/jettison-1.3.6.jar",
                                      "${SIRIUS_LIB_PATH}/mimepull-1.9.3.jar"
                                    ]
                        },
                        {"Sirius-SL":[
                                      "${SIRIUS_LIB_PATH}/asm-3.1.jar",
                                      "${SIRIUS_LIB_PATH}/axis.jar",
                                      "${SIRIUS_LIB_PATH}/commons-codec-1.7.jar",
                                      "${SIRIUS_LIB_PATH}/commons-discovery-0.2.jar",
                                      "${SIRIUS_LIB_PATH}/commons-fileupload-1.2.2.jar",
                                      "${SIRIUS_LIB_PATH}/commons-io-2.1.jar",
                                      "${SIRIUS_LIB_PATH}/commons-logging.jar",
                                      "${SIRIUS_LIB_PATH}/dir.log",
                                      "${SIRIUS_LIB_PATH}/dom4j-1.6.1.jar",
                                      "${SIRIUS_LIB_PATH}/gson-2.2.2.jar",
                                      "${SIRIUS_LIB_PATH}/jackson-core-asl-1.9.2.jar",
                                      "${SIRIUS_LIB_PATH}/jackson-jaxrs-1.9.2.jar",
                                      "${SIRIUS_LIB_PATH}/jackson-mapper-asl-1.9.2.jar",
                                      "${SIRIUS_LIB_PATH}/jackson-xc-1.9.2.jar",
                                      "${SIRIUS_LIB_PATH}/jaxrpc.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-client-1.17.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-core-1.17.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-json-1.17.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-multipart-1.17.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-server-1.17.jar",
                                      "${SIRIUS_LIB_PATH}/jersey-servlet-1.17.jar",
                                      "${SIRIUS_LIB_PATH}/jsr311-api-1.1.1.jar",
                                      "${SIRIUS_LIB_PATH}/mimepull-1.6.jar",
                                      "${SIRIUS_LIB_PATH}/poi-3.9-20121203.jar",
                                      "${SIRIUS_LIB_PATH}/poi-ooxml-3.9-20121203.jar",
                                      "${SIRIUS_LIB_PATH}/poi-ooxml-schemas-3.9-20121203.jar",
                                      "${SIRIUS_LIB_PATH}/saaj.jar",
                                      "${SIRIUS_LIB_PATH}/wsdl4j.jar",
                                      "${SIRIUS_LIB_PATH}/xmlbeans-2.3.0.jar"
                                     ]
                        }
                       ]
    if CONFIG_WAS == 'TRUE':
        #JDBC START
        SIRIUS_DB_BUSINESS = "jdbc:oracle:thin:@" + SIRIUS_DB_BUSINESS_HOST + ":" + SIRIUS_DB_BUSINESS_PORT + ":" + SIRIUS_DB_BUSINESS_NAME
        SIRIUS_LOG_DB      = "jdbc:oracle:thin:@" + SIRIUS_LOG_DB_HOST      + ":" + SIRIUS_LOG_DB_PORT      + ":" + SIRIUS_LOG_DB_NAME
        SIRIUS_LOG_DB_ARCH = "jdbc:oracle:thin:@" + SIRIUS_LOG_DB_ARCH_HOST + ":" + SIRIUS_LOG_DB_ARCH_PORT + ":" + SIRIUS_LOG_DB_ARCH_NAME
        wasMqJMSProvName = "WebSphere MQ messaging provider"
        
        mqSslConf = []
        driverName = "Oracle JDBC Driver (XA)"
        implClassName = "oracle.jdbc.xa.client.OracleXADataSource"
        XA_NONXA='true'
        try:
                if XA_TRANSACTION!='TRUE':
                        driverName="Oracle JDBC Driver (NON XA)"
                        implClassName = "oracle.jdbc.pool.OracleConnectionPoolDataSource"
                        XA_NONXA='false'
                        mqSslConf.append("-support2PCProtocol")
                        mqSslConf.append("false")
                #end if
        #end try
        except:
                pass
        #end except
        jdbcProviders=[{'driverName':driverName,
                        'implClassName':implClassName,
                        'XA_NONXA':XA_NONXA}
                       ]
        jdbcArray = [(driverName, "INFO_SCENARIO_DS",   "INFO_SCENARIO_DS",   SIRIUS_DB_BUSINESS, SIRIUS_DB_USER,          SIRIUS_DB_PASSWORD_CLIENT,          "10", "200", "100", "Sirius " + descDateTime + ""),
                     (driverName, "SIRIUS_SETTINGS_DS", "SIRIUS_SETTINGS_DS", SIRIUS_DB_BUSINESS, SIRIUS_SETTINGS_DB_USER, SIRIUS_SETTINGS_DB_PASSWORD_CLIENT, "10", "200", "100", "Sirius " + descDateTime + ""),
                     (driverName, "SIRIUS_CACHE",       "SIRIUS_CACHE",       SIRIUS_DB_BUSINESS, SIRIUS_CACHE_DB_USER,    SIRIUS_CACHE_DB_PASSWORD_CLIENT,    "10", "200", "100", "Sirius " + descDateTime + ""),
                     (driverName, "INFO_ERIB_DS",       "INFO_ERIB_DS" ,      SIRIUS_DB_BUSINESS, SIRIUS_ERIB_DB_USER,     SIRIUS_ERIB_DB_PASSWORD_CLIENT,     "10", "200", "100", "Sirius " + descDateTime + ""),
                     (driverName, "SIRIUS_LOG_DS",      "SIRIUS_LOG_DS" ,     SIRIUS_LOG_DB,      SIRIUS_LOG_DB_USER,      SIRIUS_LOG_DB_PASSWORD_CLIENT,      "10", "300", "100", "Sirius " + descDateTime + ""),
                     (driverName, "SIRIUS_LOG_ARCH_DS", "SIRIUS_LOG_ARCH_DS", SIRIUS_LOG_DB_ARCH, SIRIUS_LOG_DB_ARCH_USER, SIRIUS_LOG_DB_ARCH_PASSWORD_CLIENT, "10", "300", "100", "Sirius " + descDateTime + "")
                      ]
        #JDBC FINISH

        #JVM Settings START
        JVM_ARGS = {'-Duser.language':'en', 
                    '-Djava.net.preferIPv4Stack':'true', 
                    '-server':None, 
                    '-XX:+AggressiveOpts':None, 
                    '-XX:+AggressiveHeap':None, 
                    '-Dcom.ibm.xml.xlxp.jaxb.opti.level':'3', 
                    '-Dfile.encoding':'UTF-8',
                    '-Dsirius.log4j2.dir':'${WAS_PROPS_DIR}'
                    }
        JVM_RM_ARGS = {}
        #JVM Settings FINISH
        #MQ Settings START
        try:
                if MQ_SSL_CONF != "":
                        mqSslConf.append("-sslType")
                        mqSslConf.append("SPECIFIC")
                        mqSslConf.append("-sslConfiguration")
                        mqSslConf.append(MQ_SSL_CONF)
                #end if
        #end try
        except:
                pass
        #end except
        confactArray = [("AuditCF",    "jms/AuditCF",    MQ_MANAGER_LOG, MQ_HOST_LOG, MQ_PORT_LOG, "SC.SIRIUS" ,"Sirius "+descDateTime+ "", "100","25", "300", "TRUE"),
                        ("LogCF",      "jms/LogCF",      MQ_MANAGER_LOG, MQ_HOST_LOG, MQ_PORT_LOG, "SC.SIRIUS" ,"Sirius "+descDateTime+ "", "100","25", "300", "TRUE"),
                        ("EribDataCF", "jms/EribDataCF", MQ_MANAGER,     MQ_HOST,     MQ_PORT,     "SC.SIRIUS" ,"Sirius "+descDateTime+ "", "100","25", "300", "TRUE"),
                        ("SVCF",       "jms/SVCF",       MQ_MANAGER,     MQ_HOST,     MQ_PORT,     "SC.SIRIUS" ,"Sirius "+descDateTime+ "", "100","25", "300", "TRUE")
                       ]
        connPoolAttrs = [
                         ["connectionTimeout",     "60"],
                         ["reapTime",              "60"],
                         ["unusedTimeout",        "130"],
                         ["agedTimeout",           "60"],
                         ["purgePolicy",   "EntirePool"],
                         ["surgeThreshold",         "5"],
                         ["surgeCreationInterval", "61"],
                         ["stuckTimerTime",        "60"],
                         ["stuckTime",             "60"],
                         ["stuckThreshold",         "5"]
                        ]
                       

        queueArray = [("AuditQ",    "jms/AuditQ",    "Q.SIRIUS.AUDIT"     + sufFix +"", MQ_MANAGER_LOG, "Sirius "+descDateTime+ "","TRUE"),
                      ("LogQ",      "jms/LogQ",      "Q.SIRIUS.LOG"       + sufFix +"", MQ_MANAGER_LOG, "Sirius "+descDateTime+ "","TRUE"),
                      ("EribDataQ", "jms/EribDataQ", "Q.SIRIUS.DATA.ERIB" + sufFix +"", MQ_MANAGER,     "Sirius "+descDateTime+ "","TRUE"),
                      ("SVQ",       "jms/SVQ",       "Q.SVISTA.TO.SIRIUS" + sufFix +"", MQ_MANAGER,     "Sirius "+descDateTime+ "","TRUE")]

        lportsArray = [("AuditLP",    "jms/AuditCF",    "jms/AuditQ",    "25" ,"60", "15000", "Sirius " + descDateTime + ""),
                       ("LogLP",      "jms/LogCF",      "jms/LogQ",      "25" ,"60", "15000", "Sirius " + descDateTime + ""),
                       ("EribDataLP", "jms/EribDataCF", "jms/EribDataQ", "25" ,"60", "15000", "Sirius " + descDateTime + ""),
                       ("SVLP",       "jms/SVCF",       "jms/SVQ",       "25" ,"60", "15000", "Sirius " + descDateTime + "")]
        #MQ Settings FINISH

        #MISC Settings START
        try:
            systemLibs = SYSTEM_LIBS
        #end try
        except:
            systemLibs = SIRIUS_LIBS
        #end except
        
        try:
            newTrace=SET_NEW_TRACE
            isKeep=KEEP_TRACE_CONF
        except:
            newTrace={'*':'info'}
            isKeep='FALSE'
        #end except
        wsvarArray = [("SIRIUS_LIB_PATH",         SIRIUS_LIBS, "Sirius "+descDateTime+ "", 'FALSE'),
                      ("ORACLE_JDBC_DRIVER_PATH", systemLibs,  "Sirius "+descDateTime+ "", 'FALSE')]
        customPropArray = [("MAX.RECOVERY.RETRIES",    "500", "","false"),
                           ("RECOVERY.RETRY.INTERVAL", "30",  "","false")]

        threadPoolArray = [("WebContainer", "111", "333", "true", "1800", "Sirius " + descDateTime + "")]
        sessionManagArray = [("TuningParams", "5000", "15", "true")]
        #MISC Settings FINISH

        #SSL Settings START
        try:
            setSSL = CONFIG_SSL
        #end try
        except:
            setSSL = 'FALSE'
        #end except
        if setSSL == 'TRUE':
            #try:
            #    if SSL_MQSSL_PASS=="GENERATE":
            #        SSL_MQSSL_PASS = generate()
            #    #end if
            ##end try
            #except:
            #    SSL_MQSSL_PASS = generate()
            ##end except
            #try:
            #    if SSL_HTTPS_PASS=="GENERATE":
            #        SSL_HTTPS_PASS = generate()
            #    #end if
            ##end try
            #except:
            #    SSL_HTTPS_PASS = generate()
            ##end except
            
            sslChannels = [
                           ['SSL_2', 'HTTPS']
                           ]
#            storeConf = [
#             { 'storeCfg': ['-keyStoreName', 'MQSSL', 
#                            '-keyStoreType', 'PKCS12',
#                            '-keyStoreLocation', '$(USER_INSTALL_ROOT)\\mqssl.p12',
#                            '-keyStoreDescription', '��������� SSL ������������ ������: ' + descDateTime,
#                            '-keyStorePassword', SSL_MQSSL_PASS,
#                            '-keyStorePasswordVerify', SSL_MQSSL_PASS],
#               'certList':[
#                           ['-certificateAlias', 'sberbank_enterprise_ca_2021',
#                            '-certificateFilePath', SSL_CERTIFICATES_FOLDER + '\\' + sberbank_enterprise_ca_2021,
#                            '-base64Encoded', 'false'],
#                           ['-certificateAlias', 'sberbank_root_ca_2021',
#                            '-certificateFilePath', SSL_CERTIFICATES_FOLDER + '\\' + sberbank_root_ca_2021,
#                            '-base64Encoded', 'false']
#                            ],
#               'importList': [
#                              ['-certificateAlias', '00ca0001csiriussrs99usr',
#                               '-certificateAliasFromKeyFile', '00ca0001csiriussrs99usr',
#                               '-keyFilePath', SSL_CERTIFICATES_FOLDER + '\\' + SSL_MQSSL_SELFSTORE,
#                               '-keyFilePassword', SSL_MQSSL_SELFSTORE_PASS,
#                               '-keyFileType',SSL_MQSSL_SELFSTORE_TYPE]
#                               ]
#                 },
#             { 'storeCfg': ['-keyStoreName', 'HTTPS', 
#                            '-keyStoreType', 'PKCS12',
#                            '-keyStoreLocation', '$(USER_INSTALL_ROOT)\\https.p12',
#                            '-keyStoreDescription', '��������� SSL ������������ ������: ' + descDateTime,
#                            '-keyStorePassword', SSL_HTTPS_PASS,
#                            '-keyStorePasswordVerify', SSL_HTTPS_PASS],
#               'certList':[
#                           ['-certificateAlias', 'sberbank_enterprise_ca_2021',
#                            '-certificateFilePath', SSL_CERTIFICATES_FOLDER + '\\' + sberbank_enterprise_ca_2021,
#                            '-base64Encoded', 'false'],
#                           ['-certificateAlias', 'sberbank_root_ca_2021',
#                            '-certificateFilePath', SSL_CERTIFICATES_FOLDER + '\\' + sberbank_root_ca_2021,
#                            '-base64Encoded', 'false'],
#                           ['-certificateAlias', 'erib_datapower',
#                            '-certificateFilePath', SSL_CERTIFICATES_FOLDER + '\\' + erib_datapower,
#                            '-base64Encoded', 'false'],
#                           ['-certificateAlias', 'intermediate_pem1',
#                            '-certificateFilePath', SSL_CERTIFICATES_FOLDER + '\\' + intermediate_pem1,
#                            '-base64Encoded', 'false'],
#                           ['-certificateAlias', 'intermediate_pem2',
#                            '-certificateFilePath', SSL_CERTIFICATES_FOLDER + '\\' + intermediate_pem2,
#                            '-base64Encoded', 'false'],
#                           ['-certificateAlias', 'root_pem',
#                            '-certificateFilePath', SSL_CERTIFICATES_FOLDER + '\\' + root_pem,
#                            '-base64Encoded', 'false'],
#                            ],
#               'importList': [
#                              ['-certificateAlias', 'sirius_multserver',
#                               '-certificateAliasFromKeyFile', 'sirius_multserver',
#                               '-keyFilePath', SSL_CERTIFICATES_FOLDER + '\\' + SSL_HTTPS_SELFSTORE,
#                               '-keyFilePassword', SSL_HTTPS_SELFSTORE_PASS,
#                               '-keyFileType',SSL_HTTPS_SELFSTORE_TYPE],
#                              ['-certificateAlias', 'erib-client.ca.sbrf.ru',
#                               '-certificateAliasFromKeyFile', 'erib-client.ca.sbrf.ru',
#                               '-keyFilePath', SSL_CERTIFICATES_FOLDER + '\\' + SSL_HTTPS_SELFSTORE,
#                               '-keyFilePassword', SSL_HTTPS_SELFSTORE_PASS,
#                               '-keyFileType',SSL_HTTPS_SELFSTORE_TYPE]                               
#                               ]
#                }
#             ]
            sslConfigurations = [
                {'alias': 'MQSSL', 
                 'sslProtocol':'SSL',
                 'securityLevel': 'CUSTOM', 
                 'enabledCiphers': '[SSL_RSA_WITH_RC4_128_MD5]', 
                 'clientAuthenticationSupported': 'true',
                 'clientKeyAlias': MQSSL_ClientKey,
                 'serverKeyAlias': MQSSL_ServerKey,
                 'trustStoreName': 'MQSSL',
                 'keyStoreName': 'MQSSL'},
                {'alias': 'HTTPS', 
                 'clientKeyAlias': HTTPS_ClientKey,
                 'serverKeyAlias': HTTPS_ServerKey,
                 'trustStoreName': 'HTTPS',
                 'keyStoreName': 'HTTPS'}
                 ]
            dynamicConfigurations = [
                {'-dynSSLConfigSelectionName': 'HTTPS_ERIB',
                 '-dynSSLConfigSelectionDescription': '�������������� � �� ���� ['+descDateTime+']',
                 '-dynSSLConfigSelectionInfo': '*,*,5333|*,*,5533',
                 '-sslConfigName': 'HTTPS',
                 '-certificateAlias': HTTPS_ERIB_Cert}
                 ]
        #end if
        #SSL Settings FINISH
    #end if
    if INSTALL_APPS == 'TRUE':
        sharedLibsMapArray = [("Arm","Sirius-SL"),("sirius-arm-server","SiriusSL"),("sirius-arm-server-test","SiriusSL")]
    #end if
#end try
except:
    err_message=''
    err_message+="".rjust(37) + str(sys.exc_info()[1])
    message= "FATAL ERROR: Unexpected error while building Environment: \n%s" %  (err_message)
    print (message)
    log2file('write', message)
    log2file('close', '\n')
    raise
#end except
