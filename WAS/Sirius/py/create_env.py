'''
Last Update 2016 03 25

@author: sbt-orlov-pa
@modified by: sbt-al-gurabi-ia

'''

_modules = [
            'sys',
            'time',
            're',
            'glob',
            'os',
            'os.path',
            'getopt',
            'traceback',
            'sys.path',
            'java',
            'codecs',
            'socket'
           ]

for module in _modules:
    try:
        locals()[module] = __import__(module, {}, {}, [])
    #end try
    except ImportError:
        print 'Error importing %s.' % module
    #end except
#end for

try:
    AdminConfig = sys._getframe(1).f_locals['AdminConfig']
    AdminApp = sys._getframe(1).f_locals['AdminApp']
    AdminControl = sys._getframe(1).f_locals['AdminControl']
    AdminTask = sys._getframe(1).f_locals['AdminTask']
    #AdminUtilities = sys._getframe(1).f_locals['AdminUtilities']
    #AdminNodeManagement = sys._getframe(1).f_locals['AdminNodeManagement']
#end try
except:
    print "Warning: Caught exception accessing Admin objects. Continuing."
#end except

def _SAVE_(AUTOSAVE):
    global defname
    if AUTOSAVE == 'TRUE':
        message = "Savin' Changes"
        log.debug (message, defname)
        AdminConfig.save()
    #end if
#end _SAVE_

def getSysEnv(envVarName):
    global defname
    result=''
    try:
        result = java.lang.System.getenv(envVarName)
    except:
        result = None
    #log.trace(str(result),defname)    
    return result
#end getSysEnv

# convert param string "param1=param1Value, param2=param2Value, ..." to list
def convertParamStringToList(paramString):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    if (len(paramString) > 0):
        paramString1 = str(paramString)
        newlist = []
        if (paramString1.startswith("[[") == 0 and paramString1.endswith("]]") == 0):
            if (paramString1.find(",") > 0):
                paramString1 = paramString1.split(",")
                log.trace(str(paramString1),defname)
                for param in paramString1:
                    param = param.strip().split("=")
                    newlist1 = []
                    for p in param:
                        newlist1.append(p.strip())
                    #end for
                    newlist.append(newlist1)
                #end for
            #end if
            else:
                paramString1 = paramString1.split('=')
                newlist1 = []
                for param in paramString1:
                    newlist1.append(param.strip())
                #end for
                newlist.append(newlist1)
            #end else
            paramString = newlist
        #end if
    #end if
    log.debug(str(paramString),defname)
    defname = localdef
    return paramString
#end convertParamStringToList

def get_custom_property(config, property_name, conf_attribute='properties'):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    existing_props = []
    log.trace('AdminConfig.showAttribute(%s,%s)' %(config,conf_attribute), defname)
    properties = AdminConfig.showAttribute(config,conf_attribute)
    if not properties:
        log.debug(str(existing_props),defname)
        defname = localdef    
        return existing_props
    #end if
    properties = properties[1:len(properties)-1]
    for p in properties.split():
        log.trace('p in properties: %s' %(str(p)),defname)
        i_p = p.find('(')
        if (i_p > -1):
          if (p[0:i_p] == property_name):
            existing_props.append(p)
          #end if
        #end if
    #end for
    log.debug(str(existing_props),defname)
    defname = localdef
    return existing_props
#end get_custom_property

def deleteJAASAlias(alias, domain=None):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    params = ['-alias',alias]
    try:
        log.trace('AdminTask.deleteAuthDataEntry(%s)' % (params),defname)
        result = AdminTask.deleteAuthDataEntry(params)
        _SAVE_("TRUE")
        log.trace('Delete Authoriztion Data Entry for [%s]: %s' % (alias, str(result)),defname)
        defname = localdef
    #end try
    except:
        log.trace('Could not delete Authoriztion Data Entry for [%s]' % (alias),defname)
        defname = localdef
        pass
    #end except
    defname = localdef
#end deleteJAASAlias

def secProv(userName, secDesc, passWord):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    info = 'Created'
    if (SIRIUS_DB_RENEW == "TRUE"):
        message =  'SIRIUS_DB_RENEW is TRUE, renewing username %s.' % (userName)
        log.debug (message, defname)
        info = 'Refreshed'
        deleteJAASAlias(userName)
    #end if
    secMgrID = AdminConfig.list( 'Security' )
    log.trace('AdminConfig.create(JAASAuthDat, %s,[[alias, %s], [description, %s],[userId, %s], [password, %s]])' %(secMgrID,userName,secDesc,userName, passWord),defname)
    jaasID = AdminConfig.create('JAASAuthData', secMgrID,[['alias', userName], ['description', secDesc],['userId', userName], ['password', passWord]])
    _SAVE_("TRUE")
    log.trace('Created Authoriztion Data Entry for [%s]: %s' % (userName, str(jaasID)),defname)
    message =  "%s DB User: %s"%(info, userName)
    log.info (message, defname)
    defname = localdef
#end secProv

def configureEndpoint(channelName, sslConfigAlias):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    SCExist = 'FALSE'
    try:
        log.trace('AdminTask.getSSLConfig([-alias, %s, -scopeName, %s])' % (sslConfigAlias,scopeName),defname)
        KSMessage = AdminTask.getSSLConfig(['-alias', sslConfigAlias, '-scopeName', scopeName])
        log.trace('SSL config for [%s]: %s' % (sslConfigAlias, str(KSMessage)),defname)
        SCExist='TRUE'
    except:
        pass
    if SCExist=='TRUE':
        sslIdsList = stringToList(AdminConfig.getid("/SSLInboundChannel:" + channelName + "/"))
        log.trace('SSL IDs list: %s' % (str(sslIdsList)),defname)
        for sslId in sslIdsList:
            log.trace('AdminConfig.modify(%s,[[sslConfigAlias, %s]])' %(sslId,sslConfigAlias),defname)
            AdminConfig.modify(sslId,[['sslConfigAlias', sslConfigAlias]])
            _SAVE_("TRUE")
        #end for
        message="Configuring SSL inbound channel (%s) to use SSL configuration [%s]" %(channelName, sslConfigAlias)
        log.info(message, defname)
    #end if
    else:
        message = 'Required SSL Config [%s] does not exist' %(sslConfigAlias)
        log.error(message, defname)
    #end else
    defname = localdef    
#end configureEndpoint

def createSSLStore(lStoreConf, cell, node):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())

    scopeName = '(cell):%s:(node):%s' %(cell,node)
    log.trace('AdminTask.listKeyStores(-scopeName, %s)' % (scopeName),defname)
    message = "Key stores for scope [%s]:\n%s" %(scopeName, AdminTask.listKeyStores('-scopeName ' + scopeName))
    log.debug (message, defname)
    storeConfig = []
    storeConfig = lStoreConf['storeCfg']
    keyStoreName = storeConfig[1]

    certList = lStoreConf['certList']
    importList = lStoreConf['importList']

    storeConfig.append('-scopeName')
    storeConfig.append(scopeName)
    message = "Key Store config: %s" %(storeConfig)
    log.debug (message, defname)
    KSCreated = 'FALSE'
    try:
        log.trace('AdminTask.deleteKeyStore([-keyStoreName, %s, -scopeName, %s])' % (keyStoreName, scopeName),defname)
        message = "AdminTask.deleteKeyStore: %s" % str(AdminTask.deleteKeyStore(['-keyStoreName', keyStoreName, '-scopeName', scopeName]))
        log.info ("Deleting Key Store [%s]" %(keyStoreName), defname)
        log.debug (message, defname)
        _SAVE_('TRUE')
    except:
        err_message=''
        err_message+="".rjust(37) + str(sys.exc_info()[1])
        log.debug ("Key Store [%s] does not exist." %(keyStoreName),defname)
        log.trace (err_message, defname)
    try:
        log.trace('AdminTask.createKeyStore(%s)' % (storeConfig),defname)
        message = "AdminTask.createKeyStore: %s" % str(AdminTask.createKeyStore(storeConfig))
        KSCreated='TRUE'
        log.info ("Creating SSL Key Store [%s]" %(keyStoreName), defname)
        log.debug (message, defname)
        _SAVE_("TRUE")
    except:
        KSCreated = 'FALSE'
        err_message=''
        err_message+="".rjust(37) + str(sys.exc_info()[1])
        message = "Could not create SSL Key Store [%s]:\n%s" %(keyStoreName, err_message)
        log.error (message, defname)

    if KSCreated == 'TRUE':
        for certConfig in certList:
            certConfig.append('-keyStoreName')
            certConfig.append(keyStoreName)
            certConfig.append('-keyStoreScope')
            certConfig.append(scopeName)
            message = "Certificate config: %s" %(certConfig)
            log.debug (message, defname)
            try:
                log.trace('AdminTask.addSignerCertificate(%s)' % (certConfig),defname)
                message = "AdminTask.addSignerCertificate: %s" %(AdminTask.addSignerCertificate(certConfig))
                log.info ("Adding certificate to key store [%s]" %keyStoreName, defname)
                log.debug(message, defname)
            except:
                err_message=''
                err_message+="".rjust(37) + str(sys.exc_info()[1])
                message = "Could not add certificate [%s] to keystore [%s]:\n%s" %(certConfig[1], keyStoreName, err_message)
                log.error (message, defname)
            _SAVE_("TRUE")
        #end for

        for certConfig in importList:
            certConfig.append('-keyStoreName')
            certConfig.append(keyStoreName)
            certConfig.append('-keyStoreScope')
            certConfig.append(scopeName)
            message = "Certificate config: %s" %(certConfig)
            log.debug (message, defname)
            try:
                log.trace('AdminTask.importCertificate(%s)' % (certConfig),defname)
                message = "AdminTask.importCertificate: %s" %(AdminTask.importCertificate(certConfig))
                log.info ("Importing private certificate to key store [%s]" % keyStoreName, defname)
                log.debug (message, defname)
                _SAVE_("TRUE")
            except:
                err_message=''
                err_message+="".rjust(37) + str(sys.exc_info()[1])
                message = "IMPORT: Could not add certificate [%s] to keystore [%s]:\n%s" %(certConfig[1], keyStoreName, err_message)
                log.error (message, defname)
        #end for
    #end if
    defname = localdef    
#end createtrustStore

def createSSLConfig(sslConfiguration, cell, node):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    sslConfig=[]
    for key in sslConfiguration.keys():
        sslConfig.append('-'+key)
        sslConfig.append(sslConfiguration[key])
    #end for
    #sslConfig = sslConfiguration
    sslConfAlias = sslConfiguration['alias']
    sslConfKStore = sslConfiguration['keyStoreName']
    sslConfTStore = sslConfiguration['trustStoreName']
    
    scopeName = '(cell):%s:(node):%s' %(cell,node)

    KSExist='FALSE'
    try:
        log.trace('AdminTask.getKeyStoreInfo([-keyStoreName, %s, -scopeName, %s])' % (sslConfKStore, scopeName),defname)
        KSMessage = AdminTask.getKeyStoreInfo(['-keyStoreName', sslConfKStore, '-scopeName', scopeName])
        log.trace('AdminTask.getKeyStoreInfo([-keyStoreName, %s, -scopeName, %s])' % (sslConfTStore, scopeName),defname)
        TSMessage = AdminTask.getKeyStoreInfo(['-keyStoreName', sslConfTStore, '-scopeName', scopeName])
        KSExist='TRUE'
    except:
        pass
    
    if KSExist=='TRUE':
        sslConfig.append('-scopeName')
        sslConfig.append(scopeName)
        sslConfig.append('-trustStoreScopeName')
        sslConfig.append(scopeName)
        sslConfig.append('-keyStoreScopeName')
        sslConfig.append(scopeName)

        if currentEnv == 'serverEnv':
            keyManagerScopeName = scopeName
        #end if
        elif currentEnv == 'clusterEnv':
            keyManagerScopeName = '(cell):%s' %(cell)
        #end elif
        sslConfig.append('-keyManagerScopeName')
        sslConfig.append(keyManagerScopeName)
        log.trace('AdminTask.listSSLConfigs([-scopeName, %s, -displayObjectName, false])' % (scopeName), defname)
        message = "\nScope: %s \nSSL Configuration list: \n%s\n" %(scopeName, AdminTask.listSSLConfigs(['-scopeName', scopeName, '-displayObjectName', 'false']))
        log.debug (message, defname)
        try:
            log.trace('AdminTask.deleteSSLConfig([-alias, %s, -scopeName, %s])' % (sslConfAlias, scopeName), defname)
            message = "AdminTask.deleteSSLConfig: %s" % str(AdminTask.deleteSSLConfig(['-alias', sslConfAlias, '-scopeName', scopeName]))
            log.info("Deleting SSLConfig [%s]" %(sslConfAlias),defname)
            log.debug (message, defname)
            _SAVE_("TRUE")
        except:
            message = "SSLConfig [%s] doesn't exist" %(sslConfAlias)
            log.info (message, defname)
        try:
            log.trace('AdminTask.createSSLConfig(%s)' % (sslConfig), defname)
            message = "AdminTask.createSSLConfig: %s" % str(AdminTask.createSSLConfig(sslConfig))
            log.info ("Created SSLConfig [%s]" %(sslConfAlias), defname)
            log.debug (message, defname)
            _SAVE_("TRUE")
        except:
            err_message=''
            err_message+="".rjust(37) + str(sys.exc_info()[1])
            message = "Could not create SSLConfig [%s]:\n%s" %(sslConfAlias, err_message)
            log.error (message, defname)
    #end if
    else:
        message = 'Required keyStore [%s] or trustStore [%s] does not exist' %(sslConfKStore,sslConfTStore)
        log.error (message, defname)
    #end else
    
    
    defname = localdef
#end createSSLConfig

def createDynamicSSL(sslConfiguration, cell, node):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    sslConfig = []
    for key in sslConfiguration.keys():
        sslConfig.append(key)
        sslConfig.append(sslConfiguration[key])
    #end for
    
    sslConfAlias = sslConfiguration['-dynSSLConfigSelectionName']
    sslConfName = sslConfiguration['-sslConfigName']
    
    scopeName = '(cell):%s:(node):%s' %(cell,node)
    SCExist = 'FALSE'
    try:
        log.trace('AdminTask.getSSLConfig([-alias, %s, -scopeName, %s])' % (sslConfName, scopeName), defname)
        KSMessage = AdminTask.getSSLConfig(['-alias', sslConfName, '-scopeName', scopeName])
        SCExist='TRUE'
    except:
        pass
    
    if SCExist=='TRUE':
        sslConfig.append('-scopeName')
        sslConfig.append(scopeName)
        sslConfig.append('-sslConfigScope')
        sslConfig.append(scopeName)
        if currentEnv == 'serverEnv':
            keyManagerScopeName = scopeName
        #end if
        elif currentEnv == 'clusterEnv':
            keyManagerScopeName = '(cell):%s' %(cell)
        #end elif
        log.trace('AdminTask.listDynamicSSLConfigSelections([-scopeName, %s, -all, true])' % (scopeName), defname)
        message = "\nScope: %s \nDynamic SSL Configuration list: \n%s\n" %(scopeName, AdminTask.listDynamicSSLConfigSelections(['-scopeName', scopeName, '-all', 'true']))
        log.debug (message, defname)
        #end for
        try:
            log.trace('AdminTask.deleteDynamicSSLConfigSelection([-dynSSLConfigSelectionName, %s, -scopeName, %s])' % (sslConfAlias, scopeName), defname)
            message = "AdminTask.deleteDynamicSSLConfigSelection: %s" % str (AdminTask.deleteDynamicSSLConfigSelection(['-dynSSLConfigSelectionName', sslConfAlias, '-scopeName', scopeName]))
            log.info ("Dynamic SSLConfig [%s] deleted" %(sslConfAlias), defname)
            log.debug (message, defname)
            _SAVE_("TRUE")
        except:
            message = "Dynamic SSLConfig [%s] doesn't exist" %(sslConfAlias)
            log.info (message, defname)
        try:
            log.trace('AdminTask.createDynamicSSLConfigSelection(%s)' % (sslConfig), defname)
            message = "AdminTask.createDynamicSSLConfigSelection: %s" % str(AdminTask.createDynamicSSLConfigSelection(sslConfig))
            log.info ("Created Dynamic SSLConfig [%s]" %(sslConfAlias), defname)
            log.debug (message, defname)
            _SAVE_("TRUE")
        except:
            err_message=''
            err_message+="".rjust(37) + str(sys.exc_info()[1])
            message = "Could not create Dynamic SSLConfig [%s]:\n%s" %(sslConfAlias, err_message)
            log.error (message, defname)
    #end if
    else:
        message = 'Required SSL Config [%s] does not exist' %(sslConfName)
        log.error (message, defname)
    #end else
    defname = localdef
#end createDynamicSSL

def setTraceLevel(newTrace={'*':'info'},isKeep='FALSE'):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    
    traceService = stringToList(AdminControl.queryNames('type=TraceService,*'))
    log.trace (str(traceService), defname)
    for trace in traceService:
        log.trace ("AdminControl.getAttribute(%s, traceSpecification).split(:)" %(trace), defname)
        enabledtraces = AdminControl.getAttribute(trace,'traceSpecification').split(':')
        message = "Current trace: %s" %(enabledtraces)
        log.debug (message, defname)
        if isKeep=='TRUE':
            for parameter in enabledtraces:
                pair=parameter.split('=')
                if not pair[0] in newTrace.keys():
                    newTrace[pair[0]]=pair[1]
            #end for
        #end if
        traceSpecification=[]
        for key in newTrace.keys():
            traceSpecification.append(key + '=' + newTrace[key]+'=enabled')
        #end for
        log.trace ("AdminControl.setAttribute(%s, traceSpecification), :.join(%s)" %(trace,traceSpecification), defname)
        AdminControl.setAttribute(trace,'traceSpecification',':'.join(traceSpecification))
        _SAVE_("TRUE")
        log.trace ("AdminControl.getAttribute(%s, traceSpecification).split(:)" %(trace), defname)
        enabledtraces = AdminControl.getAttribute(trace,'traceSpecification').split(':')
        message = "New trace: %s" %(enabledtraces)
        log.info (message, defname)
    #end for
    defname = localdef    
#end setTraceLevel

def createDataSource():
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    
    def dsCreate(dsName, dsjndiName, dsUrl, userName, passWord, dsMincpool, dsMaxcpool, dsStmcache, dsDesc, jdbcProviderName):
        global defname
        localdef = defname
        defname+=" [%s]" %(callerName())

        log.trace('AdminConfig.getid(/JDBCProvider:+%s+/)' %(jdbcProviderName),defname)
        jdbcDataProvider = AdminConfig.getid('/JDBCProvider:'+jdbcProviderName+'/')
        log.trace ("jdbcDataProvider: %s" % str(jdbcDataProvider), defname)
        secDesc = dsDesc
        secProv(userName, secDesc, passWord)

        properties = [[["name", "URL"], ["type", "java.lang.String"], ["value", dsUrl]]]
        mappingAttrs = [["mapping",[ ['authDataAlias', userName],['mappingConfigAlias', 'DefaultPrincipalMapping']]]]
        connpoolAttrs = [["connectionPool",[ ['minConnections', dsMincpool],['maxConnections', dsMaxcpool],['purgePolicy', 'EntirePool'],["agedTimeout","86400"]]]]
        staticAttrs = [['authMechanismPreference', 'BASIC_PASSWORD'], ['logMissingTransactionContext','TRUE'], ['datasourceHelperClassname', "com.ibm.websphere.rsadapter.Oracle11gDataStoreHelper"], ['providerType', jdbcProviderName]]
        otherAttrsList = [['description', dsDesc], ['statementCacheSize',dsStmcache], ['jndiName', dsjndiName], ['xaRecoveryAuthAlias', userName], ['authDataAlias', userName], ['propertySet', [["resourceProperties", properties]]]]

        log.trace('AdminConfig.getid(%s + JDBCProvider:+%s+/)' %(scope,jdbcProviderName),defname)
        parentIDs = AdminConfig.getid(scope+"JDBCProvider:"+jdbcProviderName+"/")
        log.trace ("parentIDs: %s" % str(parentIDs), defname)
        requiredAttrs = [["name", dsName]]
        otherAttrsList = convertParamStringToList(otherAttrsList)
        finalAttrs = requiredAttrs+staticAttrs+otherAttrsList+mappingAttrs+connpoolAttrs
        log.trace("AdminConfig.create(DataSource, %s, %s)" % (parentIDs,finalAttrs),defname)
        newDs = str(AdminConfig.create("DataSource", parentIDs, finalAttrs))
        log.trace("AdminConfig.create: %s" % newDs,defname)
        info='Created'
        if (SIRIUS_DB_RENEW == "TRUE"):
            info='Refreshed'
        message =  "%s DataSource [%s]" % (info, dsName)
        defname = localdef
        return message
    #end dsCreate

    for jbcProvider in jdbcProviders:
        jdbcProviderName = jbcProvider['driverName']
        log.trace('AdminConfig.getid(/JDBCProvider:+%s+/)' %(jdbcProviderName),defname)
        currentDataProvider = AdminConfig.getid('/JDBCProvider:'+jdbcProviderName+'/')
        log.trace("currentDataProvider: %s" % str(currentDataProvider),defname)
        if len(currentDataProvider) == 0:
            message =  'Creating %s' % (jdbcProviderName)
            log.trace('AdminConfig.getid(%s)' %(scope),defname)
            serverID = AdminConfig.getid(scope)
            log.trace("serverID: %s" % str(serverID),defname)
            name = ['name', jdbcProviderName]
            implCN = ['implementationClassName', jbcProvider['implClassName']]
            description = ['description', jdbcProviderName]
            providerType = ['providerType', jdbcProviderName]
            classpath = ['classpath', '${ORACLE_JDBC_DRIVER_PATH}/ojdbc6.jar ${ORACLE_JDBC_DRIVER_PATH}/orai18n.jar']
            jdbcAttrs = [name, implCN, description, classpath, ['xa', jbcProvider['XA_NONXA']]]
            log.trace('AdminConfig.create(JDBCProvider, %s, %s)' %(serverID, jdbcAttrs),defname)
            currentDataProvider = AdminConfig.create('JDBCProvider', serverID, jdbcAttrs)
            log.info (message, defname)
            log.trace ("AdminConfig.create: %s" % str(currentDataProvider), defname)
        #end if
        else:
            message =  'JDBC Provider [%s]  already exists.' % (jdbcProviderName)
            log.debug (message, defname)
    #end else
    
    for dsJDBC in jdbcArray:
        jdbcProviderName = dsJDBC[0]
        dsName = dsJDBC[1]
        dsjndiName = dsJDBC[2]
        dsUrl = dsJDBC[3]
        userName = dsJDBC[4]+'_CLIENT'
        passWord = dsJDBC[5]
        dsMincpool = dsJDBC[6]
        dsMaxcpool = dsJDBC[7]
        dsStmcache = dsJDBC[8]
        dsDesc = dsJDBC[9]
        log.trace ("AdminConfig.getid(/DataSource: + %s + /)" % (dsName), defname)
        testDSName = AdminConfig.getid('/DataSource:'+dsName+'/')
        log.trace ("AdminConfig.getid: %s" % str(testDSName), defname)
        isCreateDS = 'FALSE'
        deleted=''        
        if len(testDSName)==0:
            message =  'DataSource [%s] NOT Found' % (dsName)
            log.debug (message, defname)
            isCreateDS = 'TRUE'
        #end if
        else:
            message =  'DataSource [%s] already exists.' % (dsName)
            if (SIRIUS_DB_RENEW == "TRUE"):
                message = str(objDel('DataSource', testDSName))
                log.debug (message, defname)
                isCreateDS = 'TRUE'
                _SAVE_('TRUE')
            #end if
        #end else

        
        if isCreateDS == 'TRUE':
            message = dsCreate(dsName, dsjndiName, dsUrl, userName,passWord, dsMincpool, dsMaxcpool, dsStmcache, dsDesc, jdbcProviderName)
            log.info (message, defname)            
        #end if
    #end for
    defname = localdef
#end createDataSource

def showDataSources():
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    jdbcProviderName=''
    
    for jdbcProvider in jdbcProviders:
        jdbcProviderName = jdbcProvider['driverName']
        log.trace ("AdminConfig.getid(%s + JDBCProvider: + %s + /)" % (scope,jdbcProviderName), defname)
        parentIDs = AdminConfig.getid(scope+"JDBCProvider:"+jdbcProviderName+"/")
    #end for
    log.trace("jdbcProviderName: %s" % str(jdbcProviderName),defname)
    log.trace("parentIDs: %s" % str(parentIDs),defname)
    DSources = stringToList(AdminConfig.list('DataSource'))
    log.trace("DataSource: %s" % str(DSources),defname)
    for dataSource in DSources:
        log.trace ("AdminConfig.showAttribute(%s, name)" % (dataSource), defname)
        dsName = AdminConfig.showAttribute(dataSource, 'name')
        config_id = '/JDBCProvider:%s/DataSource:%s/J2EEResourcePropertySet:/J2EEResourceProperty:/' %(jdbcProviderName, dsName)
        log.trace ("AdminConfig.getid(%s)" % (config_id), defname)
        JDBC_connectString =  AdminConfig.getid(config_id)
        log.trace("JDBC connectString [%s]: %s" % (dsName, str(JDBC_connectString)),defname)
        if len(JDBC_connectString)!=0:
            JDBCProperties = stringToList(AdminConfig.show(JDBC_connectString),'TRUE')
            log.trace("JDBCProperties: %s" % str(JDBCProperties),defname)
            message = '[%s] has connection string: %s' %(dsName, JDBCProperties['value'])
            log.info(message,defname)
        #end if
    #end for
    defname = localdef
#end showDataSources

def createConnFactory():
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    message =  "Using %s" % (wasMqJMSProvName)
    log.info (message, defname)
    log.trace ("AdminConfig.getid(%s)" % (scope), defname)
    mqJmsProv = AdminConfig.getid(scope)
    log.trace ("AdminConfig.getid: %s" % str(mqJmsProv), defname)
    log.trace('AdminTask.listWMQConnectionFactories(%s, [-type, CF])' % (mqJmsProv), defname)
    cfList=stringToList(AdminTask.listWMQConnectionFactories(mqJmsProv, ["-type", "CF"]))
    checkCF={}
    log.trace ("AdminTask.listWMQConnectionFactories: %s" % str(cfList), defname)
    for item in cfList:
        log.trace ("AdminConfig.showAttribute(%s, jndiName)" % (item), defname)
        checkCF[ AdminConfig.showAttribute(item,'jndiName')] = item
    #end for
    
    for confactory in confactArray:
        connfName        = confactory[0]
        connfjName       = confactory[1]
        connfmqName      = confactory[2]
        connfmqHost      = confactory[3]
        connfmqPort      = confactory[4]
        connfmqChan      = confactory[5]
        connfmqDesc      = confactory[6]
        connfmqBatchSize = confactory[7]
        connfmqminConn   = confactory[8]
        connfmqMaxConn   = confactory[9]
        connfDelete      = confactory[10]
        isCreateCF = 'TRUE'
        if (connfjName in checkCF.keys()):
            message =  "Remove [%s] is %s" % (connfjName, connfDelete)
            log.debug (message, defname)
            if (connfDelete == 'TRUE' ):
                log.trace('AdminTask.deleteWMQConnectionFactory(%s)' % (checkCF[connfjName]), defname)
                result = AdminTask.deleteWMQConnectionFactory(checkCF[connfjName])
                log.trace("AdminTask.deleteWMQConnectionFactory: %s" % str(result), defname)
                _SAVE_("TRUE")
            #end if
            else:
                isCreateCF='FALSE'
            #end else
        #end if

        if isCreateCF == 'TRUE':
            connfProps = ["-name", connfName,
                          "-jndiName", connfjName,
                          "-description", connfmqDesc,
                          "-qmgrName", connfmqName,
                          "-wmqTransportType", "BINDINGS_THEN_CLIENT",
                          "-qmgrHostname", connfmqHost,
                          "-qmgrPortNumber", connfmqPort,
                          "-mappingAlias", "DefaultPrincipalMapping",
                          "-qmgrSvrconnChannel", connfmqChan,
                          "-type", "CF",
                          "-maxBatchSize", connfmqBatchSize,
                          "-modelQueue", "SYSTEM.DEFAULT.MODEL.QUEUE"]
            for item in mqSslConf:
                connfProps.append(item)
            #end for
            
            connPoolAttrs.append(["minConnections", connfmqminConn])
            connPoolAttrs.append(["maxConnections",connfmqMaxConn])
            
            log.trace('AdminTask.createWMQConnectionFactory(%s, %s)' % (mqJmsProv, connfProps), defname)
            connFactory = AdminTask.createWMQConnectionFactory(mqJmsProv, connfProps)
            message = "MQ Manager Name %s, MQ Port %s, MQ Host %s, MQ Channel %s"  % (connfmqName,connfmqPort, connfmqHost, connfmqChan)
            log.debug (message, defname)
            message =  "Batch Size %s, Minimum Connections %s, Maximum Connections %s" % (connfmqBatchSize, connfmqminConn, connfmqMaxConn)
            log.debug (message, defname)
            log.trace("AdminTask.createWMQConnectionFactory: %s" % str(connFactory), defname)
            #result = AdminConfig.modify(connFactory,[["sessionPool",sessPoolAttrs]])
            log.trace ("AdminConfig.modify(%s, ,[[connectionPool, %s]])" % (connFactory,connPoolAttrs), defname)
            result = AdminConfig.modify(connFactory,[["connectionPool",connPoolAttrs]])
            log.trace("AdminConfig.modify: %s" % str(result), defname)
            message = "Created Connection Factory [%s] with JNDIName %s" % (connfName, connfjName)
            log.info (message, defname)
            _SAVE_("TRUE")
        #end if
        else:
            message =  "Connection Factory with name %s already exists." % (connfName)
            log.debug (message, defname)
        #end else
    #end while
    defname = localdef
#end createConnFactory

def createQueue():
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())

    log.trace ("AdminConfig.getid(%s)" % (scope), defname)
    mqJmsProv = AdminConfig.getid(scope)
    log.trace('AdminTask.listWMQQueues(%s)' % (mqJmsProv), defname)
    queueList = stringToList(AdminTask.listWMQQueues(mqJmsProv))
    log.trace("AdminTask.listWMQQueues: %s" % str(queueList), defname)
    
    checkQL={}
    for item in queueList:
        log.trace ("AdminConfig.showAttribute(%s, name)" % (item), defname)
        checkQL[AdminConfig.showAttribute(item,'name')]=item
    #end for
    for lenq in queueArray:
        queueName = lenq[0]
        queuejName = lenq[1]
        queuemqName = lenq[2]
        queuemqAdmin = lenq[3]
        queueDesc = lenq[4]
        queueDel = lenq[5]
        isCreateQ = 'TRUE'
        if queueName in checkQL.keys():
            message =  "Remove [%s] is %s" % (queueName, queueDel)
            log.debug (message, defname)
            if (queueDel == 'TRUE' ):
                log.trace('AdminTask.deleteWMQQueue(%s)' % (checkQL[queueName]), defname)
                result = AdminTask.deleteWMQQueue(checkQL[queueName])
                log.trace("AdminTask.deleteWMQQueue: %s" % str(result), defname)
                _SAVE_("TRUE")                
            #end if
            else:
                isCreateQ = 'FALSE'
            #end else
        #end for

        if isCreateQ == 'TRUE':
            queueProps = ["-name", queueName,
                          "-jndiName", queuejName,
                          "-description",queueDesc,
                          "-queueName",queuemqName,
                          "-qmgr",queuemqAdmin
                          ]
            log.trace('AdminTask.createWMQQueue(%s, %s)' % (mqJmsProv, queueProps), defname)
            result = AdminTask.createWMQQueue(mqJmsProv, queueProps)
            log.trace ("AdminTask.createWMQQueue: %s" % (result), defname)
            message = "Created Queue [%s] with JNDIName %s" % (queueName, queuejName)
            log.info (message, defname)
            message = "MQ Manager Name %s, MQ Destination Queue Name %s" % (queuemqAdmin, queuemqName)
            log.debug (message, defname)            
        #end if
        else:
            message =  "Queue [%s] already exists." % (queueName)
            log.debug (message, defname)
        #end else
    #end for
    defname = localdef
#end createQueue

def createPortsNew(serversList):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    mlssl = []
    mlss = []
    for server in serversList:
        mlss = stringToList(AdminConfig.list('MessageListenerService', server))
        log.trace ("AdminConfig.showAttribute(%s, name)" % (server), defname)
        serverName = AdminConfig.showAttribute(server, 'name')
        message = "List of message listener services for server %s: \n %s" %(serverName, mlss)
        log.debug (message, defname)
        for mls in mlss:
            message = "Creating MessageListenerService for: %s" % (mls)
            log.info (message, defname)
            conf_attribute = 'properties'
            new_properties = []
            for lcp in customPropArray:
                lcpName = lcp[0]
                lcpValue = lcp[1]
                lcpDescr = lcp[2]
                lcpRequire = lcp[3]
                existing_properties = get_custom_property(mls, lcpName, conf_attribute)
                if existing_properties:
                    for existing_prop in existing_properties:
                        log.trace ("AdminConfig.remove(%s)" % (existing_prop), defname)
                        result = AdminConfig.remove(existing_prop)
                        log.trace('AdminConfig.remove(%s): %s' %(str(existing_prop), str(result)), defname)
                    #end for
                #end if
                p = [ [ 'name', lcpName ], [ 'value', lcpValue ], [ 'description', lcpDescr ], [ 'required', lcpRequire ] ]
                new_properties.append(p)
            #end for
            _SAVE_('TRUE')
            if new_properties:
                log.trace ("AdminConfig.modify(%s, [[%s, %s]])" % (mls, conf_attribute, new_properties), defname)
                result = AdminConfig.modify( mls, [[conf_attribute, new_properties]] )
                log.trace('AdminConfig.modify: %s' %(str(result)), defname)
            #end if

            lpList = stringToList(AdminConfig.showAttribute(mls, "listenerPorts"))
            log.trace('listenerPorts: %s' %(str(lpList)), defname)
            for lPort in lportsArray:
                lpName = lPort[0]
                isCreateLP = 'TRUE'
                for existingLP in lpList:
                    log.trace ("AdminConfig.showAttribute(%s, name)" % (existingLP), defname)
                    existingLPName = AdminConfig.showAttribute(existingLP, 'name')
                    if lpName==existingLPName:
                        isCreateLP='FALSE'
                    #end if
                    message = "Comparing existing LP name [%s] with new LP name [%s]" %(existingLPName, lpName)
                    log.debug (message, defname)                    
                #end for
                if isCreateLP == 'TRUE':
                    lpName = lPort[0]
                    lpcfjName = lPort[1]
                    lpqjName = lPort[2]
                    lpmaxSess = lPort[3]
                    lpmaxRetr = lPort[4]
                    lpmaxMess = lPort[5]
                    lpDesc = lPort[6]
                    message =  "Creating Listener Port [%s] for server %s" % (lpName, serverName)
                    log.info(message, defname)
                    lpAttrs = [['name',lpName],['connectionFactoryJNDIName',lpcfjName],['destinationJNDIName',lpqjName],['description',lpDesc],['maxSessions', lpmaxSess],['maxRetries', lpmaxRetr],['maxMessages',lpmaxMess]]
                    log.trace ("AdminConfig.create(ListenerPort, %s, %s)" % (mls, lpAttrs), defname)
                    lstport = AdminConfig.create('ListenerPort',mls, lpAttrs)
                    log.trace ("AdminConfig.list(StateManageable, %s)" % (lstport), defname)
                    sm = AdminConfig.list('StateManageable', lstport)
                    log.trace ("AdminConfig.modify(%s, [[initialState,START]])" % (sm), defname)
                    smm = AdminConfig.modify(sm,[['initialState','START']])
                    log.trace("AdminConfig.create: %s" % str(lstport), defname)
                #end if
                else:
                    message = "Listener Port [%s] already exists for server %s." % (lpName, serverName)
                    log.debug (message, defname)
                #end else
            #end for
        #end for
    #end for
    defname = localdef
#end createPortsNew

def createVars(currentEnv):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    
    lenvars = len(wsvarArray)
    lv=0
    varList = []
    varscopes = []
    if currentEnv == 'serverEnv':
        wsvarScope = scope[1:len(scope)-1].replace(':','=').replace('/',',')
        varscopes.append(wsvarScope)
        log.trace ("wsvarScope: %s" %(wsvarScope), defname)
        varList = stringToList(AdminConfig.getid(scope+"VariableMap:/VariableSubstitutionEntry:/"))
    #end if
    elif currentEnv == 'clusterEnv':
        clusterNames = getSome ('clusterNames', currentEnv)
        for clusterName in clusterNames:
            wsvarScope = "Cluster="+clusterName
            varscopes.append(wsvarScope)
            log.trace ("wsvarScope: %s" %(wsvarScope), defname)
            varList+=stringToList(AdminConfig.getid(scope+"VariableMap:/VariableSubstitutionEntry:/"))
        #end for
    #end elif
    log.trace("var list: %s" % varList, defname)
    checkVar={}
    for item in varList:
        log.trace ("AdminConfig.showAttribute(%s, symbolicName)" % (item), defname)
        checkVar[AdminConfig.showAttribute(item, "symbolicName")]=item
    #end for
    log.debug("Varscopes: %s" % str(varscopes), defname)
    for wsvarScope in varscopes:
        for variable in wsvarArray:
            isCreateVAR='FALSE'
            info = "Created"        
            wsvarName = variable[0]
            wsvarVal = variable[1]
            wsvarDesc = variable[2]
            wsvarRefresh = variable[3]
            if not wsvarName in checkVar.keys():
                isCreateVAR='TRUE'
            #end if
            else:
                message = 'WebSphere Variable [%s] already exist' %(wsvarName)
                if wsvarRefresh=='TRUE':
                    log.trace('AdminTask.removeVariable([-variableName, %s, -scope, %s])' % (wsvarName, wsvarScope), defname)
                    removed = AdminTask.removeVariable(['-variableName', wsvarName, '-scope', wsvarScope])
                    log.debug ("AdminTask.removeVariable: %s" % str(removed), defname)
                    info = "Refreshed"
                    isCreateVAR='TRUE'
            #end else
            if isCreateVAR=='TRUE':
                log.trace('AdminTask.setVariable([-variableName, %s, -scope, %s, -variableValue, %s, -variableDescription, %s])' % (wsvarName, wsvarScope, wsvarVal, wsvarDesc), defname)
                newVar = AdminTask.setVariable(['-variableName', wsvarName, '-scope', wsvarScope, '-variableValue', wsvarVal,'-variableDescription', wsvarDesc])
                log.debug ("AdminTask.setVariable: %s" % str(newVar), defname)
                message =  "%s WebSphere Variable [%s]" % (info, wsvarName)
            log.info (message, defname)
        #end for
    #end for
    defname = localdef
#end createVars

def jvmOptsNew(serversList):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())

    #########################################################
    # Parse JVM Args
    #########################################################
    jvm_pars=JVM_ARGS
    message= "Recomended JVM params: %s" % (str(jvm_pars))
    log.info (message, defname)
    jvm_rm_pars=JVM_RM_ARGS

    for server in serversList:
        log.trace ("AdminConfig.showAttribute(%s, name)" % (server), defname)
        serverName = AdminConfig.showAttribute(server, "name")
        message="Setting configuration for Application Server %s" % (serverName)
        log.info (message, defname)

        log.trace ("AdminConfig.list(JavaVirtualMachine, %s)" % (server), defname)
        jvm = AdminConfig.list('JavaVirtualMachine', server)
        log.trace ("AdminConfig.showAttribute(%s, genericJvmArguments)" % (jvm), defname)
        result = AdminConfig.showAttribute(jvm, 'genericJvmArguments')
        message="Current JVM Settings: %s" % (result)
        log.debug (message, defname)
        params = result.split()

        jvm_args = {}
        try:
            newJvmSettings = []
            for param in params :
                message=''
                addKey = 'TRUE'
                pair = param.split('=')
                key = pair[0]
                if len(pair)>1:
                    value = pair[1].replace('\\\\','\\')
                #end if
                else:
                    value = None
                #end else
                if key in jvm_rm_pars.keys():
                    message="Removed JVM param: %s" % (key)
                    addKey = 'FALSE'
                #end if
                if key in jvm_pars.keys():
                    #key should be updated
                    addKey = 'FALSE'
                #end if
                if addKey=='TRUE':
                    message="Keep existing JVM param: %s" % (key)
                    jvm_args[key] = value
                #end if
                if len(message)>0:
                    log.debug (message, defname)
            #end for
            for newkey in jvm_pars.keys():
                message="Updating JVM param: %s" % (newkey)
                log.debug (message, defname)
                jvm_args[newkey] = jvm_pars[newkey]
            #end for
            for allkey in jvm_args.keys():
                parameter = allkey
                if jvm_args[allkey]!=None:
                    parameter+='=' + jvm_args[allkey]
                newJvmSettings.append(parameter)
            #end for
            newJvmSettingsString = " ".join(newJvmSettings)
            message="New JVM Settings: %s" % (newJvmSettingsString)
            log.info (message, defname)

            log.trace ("AdminConfig.modify(%s, [[genericJvmArguments, %s]])" % (jvm, newJvmSettingsString), defname)
            result = AdminConfig.modify(jvm, [['genericJvmArguments', newJvmSettingsString]])
            message="JVM args set successfully"
            log.info (message, defname)
        #end try
        except:
            err_message=''
            err_message+="".rjust(37) + str(sys.exc_info()[1])
            message = "Error while setting JVM args:\n%s" %(err_message)
            log.error (message, defname)
        #end except
        #end if
    #end for
    defname = localdef
#end jvmOptsNew

def sessionManag(serversList):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())

    for sessionManager in sessionManagArray:
        smName = sessionManager[0]
        smMaxinM = sessionManager[1]
        smTo = sessionManager[2]
        smOver = sessionManager[3]
        for server in serversList:
            smIds = stringToList(AdminConfig.list('SessionManager',server))
            log.trace("SessionManager list: %s" %str(smIds), defname)
            for smId in smIds:
                log.trace ("AdminConfig.show(%s)" % (smId), defname)
                smIdname = AdminConfig.show(smId)
                smIdTPs = stringToList(AdminConfig.list(smName,smId))
                log.trace("AdminConfig.list(%s, %s): %s" % (smName,smId,smIdTPs), defname)
                for smIdTP in smIdTPs:
                    log.trace ("AdminConfig.modify(%s, [[invalidationTimeout,%s],[maxInMemorySessionCount,%s],[allowOverflow,%s]])" % (smIdTP,smTo,smMaxinM,smOver), defname)
                    AdminConfig.modify(smIdTP,[['invalidationTimeout',smTo],['maxInMemorySessionCount',smMaxinM],['allowOverflow',smOver]])
                #end for
            #end for
        #end for
    #end for
    defname = localdef
#end sessionManag

def webContainer(serversList):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    
    checkThread={}
    for server in serversList:
        webcontIds = stringToList(AdminConfig.list('ThreadPool',server))
        log.trace("AdminConfig.list('ThreadPool',%s): %s" %(str(server), str(webcontIds)), defname)
        for webcId in webcontIds:
            log.trace ("AdminConfig.showAttribute(%s, name)" % (webcId), defname)
            checkThread[AdminConfig.showAttribute(webcId, 'name')]=webcId
        #end for
    #end for

    for thread in threadPoolArray:
        wbcName = thread[0]
        wbcMin = thread[1]
        wbcMax = thread[2]
        wbcOver = thread[3]
        wbcTo = thread[4]
        wbcDesc = thread[5]
        if wbcName in checkThread.keys():
            log.trace ("AdminConfig.modify(%s, [[maximumSize,%s],[minimumSize,%s],[inactivityTimeout,%s],[isGrowable,%s],[description,%s]])" % (checkThread[wbcName],wbcMax,wbcMin,wbcTo,wbcOver,wbcDesc), defname)
            AdminConfig.modify(checkThread[wbcName],[['maximumSize',wbcMax],['minimumSize',wbcMin],['inactivityTimeout',wbcTo],['isGrowable',wbcOver],['description',wbcDesc]])
        #end if
    #end for
    
    defname = localdef
#end webContainer

def stopNodeAgent():
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    nodeAgents = stringToList(AdminControl.queryNames('type=NodeAgent,*'))
    message = 'Stopping NodeAgent %s' % (nodeAgents)
    log.debug (message, defname)
    if len(nodeAgents) == 0:
        message = 'NodeAgent already stopped'
        log.info (message, defname)
    #end if
    else:
        for nodeAgent in nodeAgents:
            if len(nodeAgent)!=0:
                message = 'NodeAgentName = %s' % (nodeAgent)
                log.info (message, defname)
                log.trace ("AdminControl.invoke(%s, stopNode)" %(nodeAgent), defname)
                result = AdminControl.invoke(nodeAgent, 'stopNode')
                log.trace("Stop nodeagent: %s" % str(result), defname)
            #end if
        #end for
    #end else
    defname = localdef
#end stopNodeAgent

def stopDmgr():
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    message = "Stopping Deployment Manager"
    log.info (message, defname)
    dmgrs = stringToList(AdminControl.queryNames("processType=DeploymentManager,*" ))
    log.trace("Deployment Managers list: %s" %(str (dmgrs)), defname)
    for server in dmgrs:
        log.trace ("AdminControl.invoke(%s, stop)" %(server), defname)
        AdminControl.invoke(server, 'stop')
        message = "Deployment Manager [%s] STOPED!" % (str(server))
        log.info (message, defname)
    #end for
    defname = localdef
#end stopDmgr

def syncNodes():
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    message="Syncing nodes"
    log.info (message, defname)
    log.trace ("AdminControl.completeObjectName(type=NodeSync,node=*,*)", defname)
    Sync1 = AdminControl.completeObjectName('type=NodeSync,node=*,*')
    log.trace("NODE Sync: %s" % str(Sync1), defname)
    if Sync1 == "":
        message="Node agent status is: stop"
        log.info (message, defname)
    #end if
    else:
        log.trace ("AdminControl.invoke(%s, sync)" %(Sync1), defname)
        AdminControl.invoke(Sync1, 'sync')
    #end else
    defname = localdef
#end syncNodes

def uninstApp(appName, _is_save):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    log.trace ("AdminConfig.getid(/Deployment: + %s + /)" % (appName), defname)
    applicationId=AdminConfig.getid("/Deployment:" + appName+"/")
    log.debug ("Application id for [%s]: %s" %(appName, str(applicationId)), defname)
    if len(applicationId)>0:
        appsInvoke('STOP', appName, currentEnv)
        try:
            message='Uninstalling application [%s]'% (appName)
            log.info (message, defname)
            log.trace ("AdminApp.uninstall(%s)" % (appName), defname)
            result = AdminApp.uninstall(appName)
            log.trace("AdminApp.uninstall(%s): %s" %(appName, str(result)), defname)
            if _is_save == 'TRUE':
                _SAVE_(AUTOSAVE = 'TRUE')
            #end if
            defname = localdef
        #end try
        except:
            log.debug (str(sys.exc_info()[1]),defname)
            message='Exception occurred! Probably application %s already deleted.'% (appName)
            log.error (message, defname)
            if _is_save == 'TRUE':
                _SAVE_(AUTOSAVE = 'TRUE')
            #end if
            pass
            defname = localdef
        #end except
    #end if
    defname = localdef
#end uninstApp

def sharedLibs(scope, slarray):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    
    log.trace ("AdminConfig.getid(%s)" % (scope), defname)
    scopeID = AdminConfig.getid(scope)
    
    for currentSL in slarray:
        sharedLibName=currentSL.keys()[0]
        sharedLibList=''
#        for sharedLib in currentSL['SiriusSL']:
#            app_path = sharedLib.replace("${SIRIUS_LIB_PATH}",SIRIUS_LIBS.replace("${WAS_INSTALL_ROOT}",WAS_HOME))
#            message = "Shared library file [%s]"%(app_path)
#            log.error (message, defname)
#            if os.path.isfile(app_path) == 1:
#                message = "Shared library file found [%s]"%(sharedLib)
#                log.debug (message, defname)
#            #end if
#            else:
#                message = "Shared library file not found [%s]"%(sharedLib)
#                log.error (message, defname)
#            #end else
#        #end for
        sharedLibList = ";".join(currentSL[sharedLibName])
        sharedlibID = sharedLibsID(sharedLibName)
        if len(sharedlibID) == 0:
            objectProps = '[[nativePath ""] [name "%s"] [isolatedClassLoader "true"] [description "%s"] [classPath "%s"]]' % (sharedLibName, "Shared libs for Sirius ARM core: "+descDateTime+ "", sharedLibList)
            log.trace ("AdminConfig.create(Library, %s, %s)" % (scopeID, objectProps), defname)
            result = AdminConfig.create('Library', scopeID, objectProps)
            log.trace("AdminConfig.create: %s" % str(result), defname)
        #end if
    #end for

    defname = localdef
#end sharedLibs

def sharedLibsID(SLlibName):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    sharedlibIDs = stringToList(AdminConfig.getid('/Library:'+SLlibName+'/'))
    log.trace ("Sharedlib ID: %s" % str(sharedlibIDs), defname)
    sltext="Creating"
    if len(sharedlibIDs) > 0:
        sltext="Refreshing"
        for sharedlibID in sharedlibIDs:
            objDel('Library', sharedlibID)
            log.debug ("SharedLibs object deleted: %s" % sharedlibID, defname)
            _SAVE_('TRUE')
        #end for
    #end else
    message="%s sharedLib entry [%s]" % (sltext, SLlibName)
    log.info (message, defname)
    defname = localdef
    return ''
#end sharedLibsID

def mapSharedLibs(appName):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    lenSLMa = 0
    message=''
    while lenSLMa < len(sharedLibsMapArray):
        SLAPPName = sharedLibsMapArray[lenSLMa][0]
        SLName = sharedLibsMapArray[lenSLMa][1]
        if SLAPPName.lower() == appName.lower():
            log.trace ("AdminApp.edit(%s, [-MapSharedLibForMod, [[.*, .*, %s]]])" % (SLAPPName,SLName), defname)
            result = AdminApp.edit(SLAPPName, ['-MapSharedLibForMod', [['.*', '.*', SLName]]])
            log.trace ("AdminApp.edit: %s" % str(result), defname)
            message='Created Map of shared libs [%s] for app [%s]' % (SLName, appName)            
            log.info (message, defname)
        #end if
        elif message == '':
            message='No Map of shared libs found for app %s' % (appName)
            log.debug (message, defname)
        #end elif
        lenSLMa+=1
    #end while    
    _SAVE_(AUTOSAVE = 'TRUE')
    defname = localdef
#end mapSharedLibs

def appsInvoke(execcmd, app, currentEnv):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    invokeline = ''
    invokelines = []
    invokelines = getSome('invokelines', currentEnv)
    log.trace('invokelines: %s' %str(invokelines), defname)
    for invokeline in invokelines:
        message="Function appsInvoke(%s) for app: %s" % (execcmd,app)
        log.debug (message, defname)
        process = getWASValue('process',invokeline)
        node = getWASValue('node',invokeline)
        cell = getWASValue('cell',invokeline)
        addOn=''
        if process!= None:
            addOn+=',process='+process
        #end if
        if node!= None:
            addOn+=',node='+node
        #end if
        if cell!= None:
            addOn+=',cell='+cell
        #end if
        log.trace ("AdminControl.completeObjectName(type=Application + %s + , name= + %s +, *)" %(addOn, app), defname)
        appstatus = AdminControl.completeObjectName('type=Application'+ addOn + ',name='+app+',*')
        log.trace('Appstatus [%s]: %s' %(app, str(appstatus)), defname)
        if execcmd == 'START' and len(appstatus)==0:
            try:
                log.trace ("AdminControl.invoke(%s, startApplication, %s, [java.lang.String])" %(invokeline, app), defname)
                result = AdminControl.invoke(invokeline, 'startApplication', app, '[java.lang.String]')
                log.trace("AdminControl.invoke: %s" % str(result), defname)
                message='Application [%s] started' % (app)
                log.info (message, defname)
            except:
                log.info (str(sys.exc_info()),defname)
                message='An error occured while starting application [%s] on [process=%s, node=%s, cell=%s]' % (app, process, node, cell)
                log.warn (message, defname)
        #end if
        elif execcmd == 'STOP' and len(appstatus)>0:
            try:
                log.trace ("AdminControl.invoke(%s, stopApplication, %s, [java.lang.String])" %(invokeline, app), defname)
                result = AdminControl.invoke(invokeline, 'stopApplication', app, '[java.lang.String]')
                log.trace("AdminControl.invoke: %s" % str(result), defname)
                message='Stopping application [%s]' % (app)
                log.debug (message, defname)
                message='Process=%s, Node=%s, Cell=%s]' % (process, node, cell)
                log.debug (message, defname)
            except:
                log.info (str(sys.exc_info()),defname)
                message='An error occured while stopping application [%s] on [process=%s, node=%s, cell=%s]' % (app, process, node, cell)
                log.error (message, defname)
        #end elif
        else:
            message="Application %s on [process=%s, node=%s, cell=%s] already %s..."% (app, process, node, cell, execcmd.lower()+"ed")
            log.debug (message, defname)
        #end else
    #end for
    defname = localdef
#end appsInvoke

def manageCluster(strCommand, currentEnv):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    clusterNames = getSome ('clusterNames', currentEnv)
    log.trace("Cluster Names: %s" % str(clusterNames), defname)
    for clusterName in clusterNames:
        """Manage the named server cluster"""
        message = "Trying to %s cluster %s" % (strCommand, clusterName)
        log.debug (message, defname)
        cellnames = getCellsName()
        log.trace("Cell Names: %s" % str(cellnames), defname)
        for cellname in cellnames:
            log.trace ("AdminControl.completeObjectName(cell=%s,type=Cluster,name=%s,*)" %(cellname, clusterName), defname)
            cluster = AdminControl.completeObjectName( 'cell=%s,type=Cluster,name=%s,*' % ( cellname, clusterName ) )
            log.trace("Cluster: %s" % str(cluster), defname)
            log.trace ("AdminControl.getAttribute(%s, state)" %(cluster), defname)
            state = AdminControl.getAttribute( cluster, 'state' )
            message = "State of %s: %s" % (clusterName, state)
            log.debug (message, defname)
            if strCommand=='STOP':
                if state != 'websphere.cluster.partial.stop' and state != 'websphere.cluster.stopped':
                    log.trace ("AdminControl.invoke(%s, stop)" %(cluster), defname)
                    result = AdminControl.invoke( cluster, 'stop')
                    log.trace("Stoping: %s" % str(result),defname)
                    # Wait for it to stop
                    maxwait = 300 # wait about 5 minutes at most
                    count = 0
                    message = "Wait for cluster %s to stop" % (clusterName)
                    log.info (message, defname)
                    while state != 'websphere.cluster.stopped':
                        time.sleep( 30 )
                        log.trace ("AdminControl.getAttribute(%s, state)" %(cluster), defname)
                        state = AdminControl.getAttribute( cluster, 'state' )
                        message = "State of %s: %s" % (clusterName, state )
                        log.debug (message, defname)
                        count += 1
                        if count > ( maxwait / 30 ):
                            message = ("Giving up waiting for [%s] to stop" %(clusterName))
                            log.warn (message, defname)
                            break
                        #end if
                    #end while                    
                #end if
            #end if
            if strCommand=='START':
                if state != 'websphere.cluster.partial.stop' and state != 'websphere.cluster.running':
                    log.trace ("AdminControl.invoke(%s, start)" %(cluster), defname)
                    result = AdminControl.invoke( cluster, 'start')
                    log.trace("Starting: %s" % str(result),defname)
                    # Wait for it to stop
                    maxwait = 300 # wait about 5 minutes at most
                    count = 0
                    message = "Wait for cluster %s to start" % (clusterName)
                    log.info (message, defname)
                    while state != 'websphere.cluster.running':
                        time.sleep( 30 )
                        log.trace ("AdminControl.getAttribute(%s, state)" %(cluster), defname)
                        state = AdminControl.getAttribute( cluster, 'state' )
                        message = "State of %s: %s" % (clusterName, state )
                        log.debug (message, defname)
                        count += 1
                        if count > ( maxwait / 30 ):
                            message = ("Giving up waiting for [%s] to start" %(clusterName))
                            log.warn (message, defname)
                            break
                        #end if
                    #end while
                #end if
            #end if
        #end for
    #end for
    defname = localdef
#end manageCluster

def installAPP(APP_LIST, currentEnv):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    AUTOSAVE = 'TRUE'

    ws_path = getSysEnv('WS')
    apps_path = getSysEnv('APP_WS')
    appsToInstall = APP_LIST
    appsToInstall = appsToInstall.split(',')
    message = "Application List For Installation: %s" % (appsToInstall)
    log.debug (message, defname)
    message = 'Applications path: %s' % (apps_path)
    log.debug (message, defname)
    
    for appToInstall in appsToInstall:
        app_path = apps_path + '\\' + appToInstall
        appName = appToInstall.rstrip()
        appName = appName.split(".")[0]
        if os.path.isfile(app_path) == 1:
            message = "uninstApp(%s, %s)" %(str(appName), str(AUTOSAVE))
            log.trace (message, defname)
            uninstApp(appName, AUTOSAVE)
            install_scopes = getSome('installscope', currentEnv)
            log.trace("install_scopes: %s" % str(install_scopes), defname)
            for install_scope in install_scopes:
                installArgs = [install_scope, "-nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -nodeployejb -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -appname "+ appName +' -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -MapModulesToServers [[ .* .* .* ]] -MapWebModToVH [[ .* .* default_host ]]']
                message = 'Installing application [%s]' %(appName)
                log.info (message, defname)
                message = "App path: %s \n Install arguments: %s" %(app_path, installArgs)
                log.debug (message, defname)
                log.trace ("AdminApp.install(%s, %s)" % (app_path,installArgs), defname)
                result = AdminApp.install(app_path, installArgs)
                log.trace("AdminApp.install(%s): %s" %(app_path, str(result)), defname)
                _SAVE_(AUTOSAVE)
            #end for
            mapSharedLibs(appName)
        #end if
        else:
            message = "File for application %s not found"%(appName)
            log.error (message, defname)
        #end else
    #end for
    defname = localdef
#end installAPP
#######

def clearCache(currentEnv):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    from java.lang import String
    import jarray

    clearContent = '<project name="cleanup" default="cleanup"> <target name="cleanup">  <delete failonerror="false" verbose="true" quiet="false" dir="${user.install.root}/temp" />  <delete failonerror="false" verbose="true" quiet="false" dir="${user.install.root}/wstemp" />  <delete failonerror="false" verbose="true" quiet="false" dir="${user.install.root}/tranlog" />  <delete failonerror="false" verbose="true" quiet="false">   <fileset dir="${user.install.root}" includes="javacore.*.txt" />  </delete> </target></project>'
    strClear = String(clearContent)
    bytesClear = strClear.getBytes()
    props = jarray.array( [], String)

    antLines = getSome('antLines', currentEnv)
    message = "antLines count is: %d" %(len(antLines))
    log.debug (message, defname)

    manageCluster("STOP", currentEnv)

    for antLine in antLines:
        strProcess=getWASValue('process',antLine)
        try:
            antAgent = getJMXMBean1(type='AntAgent', process=strProcess)
            antAgent.putScript(String('cleanup.xml'), bytesClear)
            antAgent.invokeAnt(props, String('cleanup.xml'), String('cleanup'))
            antLog=String(antAgent.getLastLog())
            message = "CAHCE cleared at %s" % (strProcess)
            log.info (message, defname)
            message = "ANT Log:\n%s" % (antLog)
            log.debug (message, defname)            
        #end try
        except:
            log.debug (str(sys.exc_info()[1]),defname)
            message = "No ANT agent for %s" % (strProcess)
            log.debug (message, defname)
        #end except
    #end for
    if STOP_SERVER != 'TRUE':
        manageCluster("START", currentEnv)
    defname = localdef
#end clearCache

try:
    script_Dir = getSysEnv('SCRIPT_DIR_NAME')+'\\'
    config_Dir = getSysEnv('CONFIG_DIR_NAME')+'\\'	

    sys.path.append(config_Dir)
    sys.path.append(script_Dir)

    import log
    from config import *
    from system import *
    from defaults import *
    from log import log2file
    from log import curTime

    global defname
    defname = 'create_env'
    
    descDateTime=""
    descDateTime = curTime("date")
    log2file('open','Open\n')
    message = "Current UTC Time is: %s" %(descDateTime)
    log.info (message, defname)
    fixupOsType()
    WAS_HOME = getSysInfo()
    currentEnv = getEnv()
    scopes = []
    scopesID = []
    scopes, scopesID = getScope(currentEnv)

    if len(scopes)==0:
        raise Exception('No scope. Check WAS installation')
    message = "[%d] Scopes are: %s" % (len(scopes),str(scopes))
    log.debug (message, defname)

    for scope in scopes:
        message = "Scope Is: %s" % (scope)
        log.info (message, defname)
        message = "CONFIG_WAS: %s" % (CONFIG_WAS)
        log.debug (message, defname)
        #showDataSources()
        if CONFIG_WAS == 'TRUE':
            message = "Starting configuring WAS"
            log.debug (message, defname)
            try:
                setSSL = CONFIG_SSL
            except:
                setSSL = 'FALSE'

            message = "CONFIG_SSL: %s" % (setSSL)
            log.debug (message, defname)
            if setSSL == 'TRUE':
                nodes = getNodesName()
                cells = getCellsName()
                for node in nodes:
                    for cell in cells:
                        #for config in storeConf:
                        #    createSSLStore(config, cell, node)
                        ##end for
                        for config in sslConfigurations:
                            createSSLConfig(config, cell, node)
                        #end for
                        for config in dynamicConfigurations:
                            createDynamicSSL(config, cell, node)
                        #end for
                    #end for
                #end for
                for channel in sslChannels:
                    configureEndpoint(channel[0], channel[1])
                #end for
            #end if
            serversList = getServerList()
            sharedLibs(scope, sharedLibsArray)
            jvmOptsNew(serversList)
            createConnFactory()
            createQueue()
            createPortsNew(serversList)
            createDataSource()
            createVars(currentEnv)
            webContainer(serversList)
            sessionManag(serversList)
            setTraceLevel(newTrace,isKeep)
            _SAVE_('TRUE')
            message = "Finished configuring WAS"
            log.debug (message, defname)
        #end if
        if INSTALL_APPS == 'TRUE':
            APP_LIST = APP_TO_INSTALL
            message = "Starting installing list of applications: %s" % (INSTALL_APPS)
            log.debug (message, defname)
            appsToUnInstall = APP_TO_UNINSTALL.split(',')
            if len(appsToUnInstall)>0 and len(APP_TO_UNINSTALL)>0:
                message = "Application List For Uninstall: '%s' [%d]" % (APP_TO_UNINSTALL, len(appsToUnInstall))
                log.debug (message, defname)
                for appToUnInstall in appsToUnInstall:
                    appName = appToUnInstall.rstrip()
                    appName = appName.split(".")[0]
                    uninstApp(appName, 'TRUE')
                #end for
            #end if
            installAPP(APP_LIST, currentEnv)
            _SAVE_('TRUE')
            message = "Finished installing list of applications"
            log.debug (message, defname)
        #end if
    #end for

    if currentEnv == 'clusterEnv':
        syncNodes()
    #end if

    if CLEAR_CACHE == 'TRUE':
        clearCache(currentEnv)
    #end if

    if STOP_SERVER == 'TRUE':
        message = "Stopping server: %s" % (STOP_SERVER)
        log.info (message, defname)
        try:
            ONLY_NODES = getSysEnv('ONLY_NODES')
            notOnlyNodes=(ONLY_NODES != 'TRUE')
        #end try
        except:
            ONLY_NODES = 'FALSE'
            notOnlyNodes=1
        #end except
        manageCluster("STOP", currentEnv)
        
        message = "ONLY_NODES: %s" %(ONLY_NODES)
        log.info (message, defname)
        
        if notOnlyNodes:
            stopNodeAgent ()
            stopDmgr()
        #end if
    #end if

    #START_SERVER - optional
    try:
        if START_SERVER == 'TRUE':
            message = "Starting server: %s" % (START_SERVER)
            log.info (message, defname)
            manageCluster("START", currentEnv)
            if currentEnv == 'clusterEnv':
                syncNodes()
            #end if
        #end if
        if SET_TRACE_LEVEL == 'TRUE':
            setTraceLevel(newTrace,isKeep)
        #end if
    #end try
    except:
        pass
    #end except
    message = 'SUCCESS: The WebSphere Application Server configuration script has successfuly ended.'
    log.info(message, defname)
    log2file('close', '\n')
#end try
except:
    err_message=''
    err_message+="".rjust(37) + str(sys.exc_info()[0])+"\n"
    err_message+="".rjust(37) + str(sys.exc_info()[1])+"\n"
    err_message+="".rjust(37) + str(sys.exc_info()[2])
    message= "FATAL ERROR: Unexpected error while building Environment:\n%s" %  (err_message)
    print(message)
    log2file('write', message + '\n')
    log2file('close', '\n')
    raise
#end except