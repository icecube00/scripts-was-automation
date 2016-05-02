'''
Last Update 2016 03 31

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
            'socket',
            'string',
            'random'
           ]


for module in _modules:
    try:
        locals()[module] = __import__(module, {}, {}, [])
    #end try
    except ImportError:
        print 'Error importing %s.' % module
    #end except
#end for

import log
from log import log2file
from log import curTime    

global defname
defname = 'system'

class JMXMBeanAttribute:
    def __init__(self, mbean, info):
        self.mbean = mbean
        self.info = info
    #end __init__

    def getValue(self):
        return AdminControl.getAttribute_jmx(
            self.mbean._objectName, self.info.name
        )
    #end getValue

    def setValue(self, value):
        AdminControl.setAttribute_jmx(
            self.mbean._objectName, self.info.name, value
        )
        return value
    #end setValue
#end JMXMBeanAttribute

class JMXMBeanOperation:
    def __init__(self, mbean, info):
        self._mbean = mbean
        self._info = info
        self._signature = []
        for t in info.signature:
            self._signature.append(t.type)
        #end for
    #end __init__

    def __call__(self, *arguments):
        return AdminControl.invoke_jmx(
            self._mbean._objectName, self._info.name, arguments,
            self._signature
        )
    #end __call__
#end JMXMBeanOperation

class JMXMBean:
    def __init__(self, _id):
        self._id = _id
        self._attributes = {}
        self._operations = {}
        self._objectName = AdminControl.makeObjectName(_id)
        mbeanInfo = AdminControl.getMBeanInfo_jmx(self._objectName)
        for attr in mbeanInfo.attributes:
            self._attributes[attr.name] = JMXMBeanAttribute(self, attr)
        #end for
        for opr in mbeanInfo.operations:
            if not self._operations.has_key(opr.name):
                self._operations[opr.name] = OperationGroup(self, opr.name)
            #end if
            group = self._operations[opr.name]
            group.addOperation(JMXMBeanOperation(self, opr))
        #end for
    #end __init__
    def __getattr__(self, name):
        if self._attributes.has_key(name):
            return self._attributes[name].getValue()
        #end if
        elif self._operations.has_key(name):
            return self._operations[name]
        #end elif
        else:
            raise AttributeError(name)
        #end else
    #end __getattr__
    def __setattr__(self, name, value):
        if name in ['_id', '_attributes', '_operations', '_objectName']:
            self.__dict__[name] = value
        #end if
        elif self._attributes.has_key(name):
            return self._attributes[name].setValue(value)
        #end elif
        else:
            raise AttributeError(name)
        #end else
    #end __setattr__
    def __str__(self):
        return self._id
    #end __str__
    def __unicode__(self):
        return unicode(self._id)
    #end __unicode__
    def __repr__(self):
        return '%s("%s")' % (self.__class__, self._id)
    #end __repr__
    def waitForNotification(
        self, typeOrTypes=None, propertiesOrPropertiesList=None, timeout=300.0
    ):
        return waitForNotification(
            self._id, typeOrTypes, propertiesOrPropertiesList, timeout
        )
    #end waitForNotification
#JMXMBean

class OperationGroup:
    def __init__(self, mbean, name):
        self._mbean = mbean
        self._operations = {}
        self._overloads = {}
        self._name = name
    #end __init__
    def __call__(self, *arguments):
        numberOfOperations = len(self._operations)
        numberOfOverloads = len(self._overloads.get(len(arguments), 0))
        # call may be ambiguous if the operation is not overloaded
        if numberOfOperations == 1:
            # if the operation isn't overloaded, then let's just proceed with
            # the call without even looking at arguments
            return apply(self._operations.values()[0], arguments)
        #end if
        elif numberOfOverloads == 1:
            # if the operation is overloaded and number of parameters matches
            # number of call arguments, then we proceed with the call without
            # checking argument types
            return apply(self._overloads[len(arguments)][0], arguments)
        #end elif
        else:
            # otherwise the operation must be first looked up using it's
            # signature:
            # mbean.operationName[['int','int']]
            raise Exception(
                'Could not match operation %s for MBean %s'
                % (self._name, self._mbean._id)
            )
        #end else
    #end __call__
    def __getitem__(self, signature):
        return self._operations[repr(tuple(signature))]
    #end __getitem__
    def addOperation(self, operation):
        signature = []
        for a in operation._info.signature:
            signature.append(a.type)
        #end for
        self._operations[repr(tuple(signature))] = operation
        overloads = list(self._overloads.get(len(signature), []))
        overloads.append(operation)
        self._overloads[len(signature)] = tuple(overloads)
    #end addOperation
#end OperationGroup

def getJMXMBean1(domain='WebSphere', **attributes):
    queryString = '%s:*' % domain
    for (k, v) in attributes.items():
        queryString += ',%s=%s' % (k, v)
    #end for
    result = stringToList(AdminControl.queryNames(queryString))
    if len(result) == 1:
        return JMXMBean(result[0])
    #end if
    elif len(result) == 0:
        raise Exception('No JMXMBean found matching query %s' % queryString)
    #end elif
    else:
        raise Exception(
            'More than one JMXMBean found matching query %s' % queryString
        )
    #end else
#end getJMXMBean1

def getSysEnv(envVarName):
    result=''
    try:
        result = java.lang.System.getenv(envVarName)
    except:
        result = None
    return result
#end getSysEnv

def fixupOsType():
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    thisOs = java.lang.System.getProperty("os.name")
    message = 'OS Name = %s' % (thisOs)
    log.info (message, defname)
    windowsServerOsPattern = r"Windows.*(2008| 7|8|2012)"
    if re.match(windowsServerOsPattern, thisOs):
        message = 'Setting OS %s to be recognized as an NT derived system' % (thisOs)
        log.debug (message, defname)
        sys.registry.setProperty("python.os", "nt")
    #end if
    defname=localdef
#end fixupOsType

def getSysInfo():
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    message = "System PATH is: %s" % sys.path
    WAS_HOME=''
    log.debug (message, defname)
    for cell in getCellsName(): 
        message = "Current cell: %s" % cell
        log.debug (message, defname)
        for node in getNodesName():
            message = "Current cell: %s" % cell
            log.debug (message, defname)
            WAS_HOME = getWASHome(cell,node)
            message = "WAS HOME is: %s" % (WAS_HOME)
            log.info (message, defname)
        #end for
    #end for
    message = "System HOSTNAME is: %s" % (socket.gethostname())
    log.info (message, defname)
    message = "System FQD_HOSTNAME is: %s" % (socket.getfqdn((socket.gethostname())))
    log.debug (message, defname)
    message = "Script executing in Domain %s from User %s@%s." % (getSysEnv('USERDOMAIN'), getSysEnv('USERNAME'),getSysEnv('USERDNSDOMAIN'))
    log.info (message, defname)
    defname=localdef
    return WAS_HOME
#end getSysInfo

def stringToList(inStr, isCollection='FALSE'):
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())

    message = '\ninStr: %s\nisCollection: %s' %(inStr,isCollection)
    log.trace(message,defname)

    inStr = inStr.rstrip();
    tmpList=[]
    if (len(inStr)>0):
        inStr = ''.join(inStr.split("\r"))
        
        if len(inStr.split("\n"))>1:
            tmpList = inStr.split("\n")
        #end if
        if len(tmpList)>1:
            tList=[]
            for value in tmpList:
                if (value[0]=='[' and value[-1]==']'):
                    value = value[1:-1]
                temp = value.split(" ")
                for tValue in temp:
                    tList.append(tValue)
            tmpList=tList
        #end if
        elif (inStr[0]=='[' and inStr[-1]==']'):
            tmpList = inStr[1:-1].split(" ")
        #end elif
        else:
            tmpList = inStr.split(" ")
    #end if
    else:
        tmpList = inStr.split("\n")   #splits for Windows or Linux
    #end else
    listLength = len(tmpList)
    currentItem=0    
    if isCollection=='TRUE':
        outList={}
        add=2
    #end if
    else:
        outList=[]
        add=1
    #end else
    while currentItem<listLength:
        if isCollection=='TRUE':
            strCurrenItem = tmpList[currentItem]
            outList[tmpList[currentItem]]=tmpList[currentItem+1]
        #end if
        else:
            strCurrenItem = currentItem
            outList.append(tmpList[currentItem])
        #end else
        currentItem+=add
        message = 'currentItem: %d\tlistLength: %d\tlen(outList): %d\n\tlist item: %s' %(currentItem,listLength,len(outList),str(outList[strCurrenItem]))
        log.trace(message,defname)
    #end while
    defname=localdef
    if len(outList)==1:
        if outList[0]=="":
            outList=[]
        #end if
    #end if
    return outList
#end stringToList

def objDel(objtype, objNameID):
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    log.debug('Trying to delete object: type:%s\tid:%s' %(objtype,objNameID), defname)
    delListObj = stringToList(AdminConfig.list(objtype))
    for delObj in delListObj:
        log.trace('Got object: %s' %str(delObj), defname)
        if str(delObj)==objNameID:
            log.trace('AdminConfig.remove(%s)' %str(delObj), defname)
            result = AdminConfig.remove(delObj)
            log.debug('AdminConfig.remove(%s): %s' % (str(delObj), str(result)), defname)
        #end if

    #end for
    defname=localdef
#end objDel

def getCellsList():
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    cellsList = stringToList(AdminConfig.list('Cell'))
    message="Cells are: %s" % str(cellsList)
    log.debug (message, defname)
    defname=localdef
    return cellsList
#end getCellsList

def getCellsName():
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    cellNames=[]
    cells = getCellsList()
    for cell in cells:
        log.trace('AdminConfig.showAttribute(%s, name)' %str(cell), defname)
        cellName = AdminConfig.showAttribute(cell, 'name')
        cellNames.append(cellName)
    #end for
    message = "Cell names are: %s" % str(cellNames)
    log.debug (message, defname)
    defname=localdef
    return cellNames
#end getCellsName

def getNodesName():
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    nodeNames = []
    nodes = stringToList(AdminControl.completeObjectName('type=NodeAgent,*'))

    message="Nodes are: %s" %(nodes)
    log.debug (message, defname)

    for node in nodes:
        message="Current node: %s" %(node)
        log.debug (message, defname)
        nodeName = getWASValue('node',node)
        nodeNames.append(nodeName)
    #end for
    message="Node names are: %s" %(nodeNames)
    log.debug (message, defname)
    defname=localdef
    return nodeNames
#end getNodesName

def getScope(gscopeEnv):
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    gscopesID = []
    gscopes = []
    if gscopeEnv=='serverEnv':
        cells = getCellsList()
        for cell in cells:
            log.trace('AdminConfig.showAttribute(%s, name)' %str(cell), defname)
            cellName = AdminConfig.showAttribute(cell, 'name')
            nodes = stringToList(AdminConfig.list('Node', cell))
            
            message = "Cell name: %s\tNodes: %s" %(cellName,nodes)
            log.debug(message, defname)
            
            for nodeName in nodes:
                log.trace('AdminConfig.showAttribute(%s, name)' %str(nodeName), defname)
                nodeID = AdminConfig.showAttribute(nodeName, 'name')
                
                message = "Node name: %s" %str(nodeID)
                log.debug(message, defname)
                
                servers = stringToList(AdminControl.queryNames('type=Server,cell=' + cellName +',node=' + nodeID + ',processType=UnManagedProcess,*'))
                for serverID in servers:
                    gscopesID.append(serverID)
                    log.trace('AdminControl.getAttribute(%s, name)' %(serverID),defname)
                    serverName = AdminControl.getAttribute(serverID, 'name')
                    scope = "/Node:"+nodeID+"/Server:"+serverName+"/"
                    gscopes.append(scope)
                #end for
            #end for
        #end for
    #end if
    else:
        clusters = stringToList(AdminConfig.list('ServerCluster'))
        log.trace('AdminConfig.list(ServerCluster)', defname)
        str_clusters=AdminConfig.list('ServerCluster')
        message =  "Server clusters are: %s" % (str_clusters)
        log.debug (message, defname)
        for clusterID in clusters:
            gscopesID.append(clusterID)
            log.trace('AdminConfig.showAttribute(%s, name)' %(clusterID), defname)
            clusterName = AdminConfig.showAttribute(clusterID, 'name')
            scope = "/ServerCluster:"+clusterName+"/"
            gscopes.append(scope)
        #end for
    #end else
    log.trace('Scopes: %s' % str(gscopes), defname)
    log.trace('Scopes IDs: %s' % str(gscopesID), defname)
    defname=localdef
    return (gscopes, gscopesID)
#end getScope

def getServerList():
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    
    log.trace('AdminTask.listServers([-serverType APPLICATION_SERVER ])',defname)
    servers = AdminTask.listServers('[-serverType APPLICATION_SERVER ]')
    log.trace('Servers: %s' % str(servers),defname)
    if (servers != ['']):
        servers = servers [0:len(servers)].splitlines()
    #end if

    defname=localdef
    return (servers)
#end getServerList

def listClusters():
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    defname=localdef
    return stringToList(AdminConfig.list('ServerCluster'))
#end listClusters

def getEnv():
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    cellnames = getCellsName()
    for cellname in cellnames:
        log.trace('AdminConfig.getid(/Cell: + %s + /)' %(cellname), defname)
        cellId = AdminConfig.getid("/Cell:" + cellname + "/")
        log.trace ('AdminConfig.getid(/Cell:%s/): %s' % (cellname, str(cellId)), defname)
        log.trace('AdminConfig.showAttribute(%s, cellType)' %(cellId), defname)
        cellType = AdminConfig.showAttribute(cellId, "cellType")
        message = "Cell type is: %s" %(cellType)
        log.info (message, defname)
        if cellType == "DISTRIBUTED":
            defname=localdef
            return 'clusterEnv'
        #end if
        elif cellType == "STANDALONE":
            defname=localdef
            return 'serverEnv'
        #end elif
    #end for
    defname=localdef
    return 'mixedEnv'
#end getEnv

def getSome(inValue, currentEnv):
    global defname
    localdef=defname
    defname+= " [getSome("+inValue+")]"
    returnValue = []
    cellNames = getCellsName()
    for cellName in cellNames:
        if inValue == 'invokelines':
            invokeline = ''
            invokelines = []
            if currentEnv == 'serverEnv':
                log.trace('AdminControl.queryNames(type=Server,cell=%s, *)' %(cellName),defname)
                serverID = AdminControl.queryNames('type=Server,cell=' + cellName + ',*')
                log.trace('AdminControl.getAttribute(%s, name)' %(serverID), defname)
                serverName = AdminControl.getAttribute(serverID, 'name')
                names='cell='+cellName+',type=ApplicationManager,process='+serverName+',*'
                log.trace('AdminControl.queryNames(%s)' %(names), defname)
                appManager = AdminControl.queryNames(names)
                message = "Getting names for: %s\n%s" %(names, appManager)
                log.debug(message, defname)
                invokelines.append(appManager)
                message = "Server Name is: %s CellName is: %s" % (serverName, cellName)
                log.debug (message, defname)
            #end if
            elif currentEnv == 'clusterEnv':
                for cluster in listClusters():
                    clusterMembers = stringToList(AdminConfig.list('ClusterMember',cluster))
                    for clusterMember in clusterMembers:
                        log.trace('AdminConfig.showAttribute(%s, memberName)' %(clusterMember), defname)
                        serverName = AdminConfig.showAttribute(clusterMember, 'memberName')
                        log.trace('AdminConfig.showAttribute(%s, nodeName)' %(clusterMember), defname)
                        nodeName = AdminConfig.showAttribute(clusterMember, 'nodeName')
                        names='WebSphere:name=ApplicationManager,process='+serverName+',cell='+cellName+',mbeanIdentifier=ApplicationManager,type=ApplicationManager,node='+nodeName+',*'
                        log.trace('AdminControl.queryNames(%s)' %(names), defname)
                        appManager = AdminControl.queryNames(names)
                        message = "Getting names for: %s\n%s" %(names, appManager) #DEBUG
                        log.debug (message, defname) #DEBUG
                        if appManager!="":
                            invokelines.append(appManager)
                    #end for
                #end for
                message = "Server Name is: %s CellName is: %s Node name: %s" % (serverName, cellName, nodeName)
                log.debug (message, defname)
            #end elif
            returnValue = invokelines
        #end if
        elif inValue == 'installscope':
            install_scopes = []
            if currentEnv == 'serverEnv':
                log.trace('AdminControl.queryNames(type=Server,cell=%s, *)' %(cellName), defname)
                serverID = AdminControl.queryNames('type=Server,cell=' + cellName + ',*')
                log.trace('AdminControl.getAttribute(%s, name)' %(serverID), defname)
                serverName = AdminControl.getAttribute(serverID, 'name')
                install_scope = '-cell %s -server %s' %(cellName,serverName)
                install_scopes.append(install_scope)
            #end if
            elif currentEnv == 'clusterEnv':
                for cluster in listClusters():
                    log.trace('AdminConfig.showAttribute(%s, name)' %(cluster), defname)
                    clusterName = AdminConfig.showAttribute(cluster, 'name')
                    install_scope='-cell %s -cluster %s'% (cellName,clusterName)
                    install_scopes.append(install_scope)
                #end for
            #end elif
            message = "Install_scopes are: %s" % (install_scopes)
            log.debug (message, defname)
            returnValue = install_scopes
        #end elif
        elif inValue == 'clusterNames':
            clusterNames = []
            if currentEnv == 'clusterEnv':
                for cluster in listClusters():
                    log.trace('AdminConfig.showAttribute(%s, name)' %(cluster), defname)
                    clusterName = AdminConfig.showAttribute(cluster, 'name')
                    clusterNames.append(clusterName)
                #end for
            #end if
            returnValue = clusterNames
            message = "Cluster names are: %s" % (clusterNames)
            log.debug (message, defname)
        #end elif
        elif inValue == 'antLines':
            antLines = []
            if currentEnv == 'serverEnv':
                log.trace('AdminControl.queryNames(WebSphere:*,type=AntAgent)', defname)
                appManager = AdminControl.queryNames('WebSphere:*,type=AntAgent')
                antLines.append(appManager)
            #end if
            elif currentEnv == 'clusterEnv':
                appManager = stringToList(AdminControl.queryNames('WebSphere:*,type=AntAgent'))
                message = "AntAgent: %s" % (appManager)
                log.debug (message, defname)
                for antLine in appManager:
                    antLines.append(antLine)
                #end for
            #end elif
            returnValue = antLines
        #end if
    #end for
    defname=localdef
    return returnValue
#end getSome

def getWASValue(paramName,wasString):
    global defname
    localdef = defname
    defname+=" [%s]" %(callerName())
    result=None
    listParams=wasString.split(':',1)
    if len(listParams)==2:
        params=listParams[1].split(',')
        for param in params:
            tmpParam = param.split("=")
            if tmpParam[0]==paramName:
                result = tmpParam[1]
                message = "Looking for %s. Got a value [%s]" %(paramName, result)
                log.trace (message, defname)
            #end if
        #end for
    #end if
    else:
        message = "Looking for %s. Could not split WAS string [%s]" %(paramName, wasString)
        log.warn (message, defname)
    #end else
    defname = localdef
    return result
#end getWASValue

def generate(size=8, chars=(string.digits + string.letters)):
    global defname
    localdef=defname
    defname+=" [%s]" %(callerName())
    log.trace('Generate [size: %d, chars: %s' %(size,chars), defname)
    
    mstr=[]
    z=0
    while z<size:
        mstr.append(random.choice(chars))
        z+=1
    result = ''.join(mstr)

    defname=localdef
    return result
#end generate

def callerName() :
  "callerName() - Returns the name of the calling routine (or '?')"
  return sys._getframe( 1 ).f_code.co_name
#end callerName

def getWASHome(cell, node):
    log.trace('AdminConfig.getid(/Cell: + %s + /Node: + %s + /VariableMap:/)' %(cell, node), defname)
    varMap = AdminConfig.getid("/Cell:" + cell + "/Node:" + node + "/VariableMap:/")
    log.trace('AdminConfig.list(VariableSubstitutionEntry, %s)' %(varMap), defname)
    entries = AdminConfig.list("VariableSubstitutionEntry", varMap)
    eList = entries.splitlines()
    for entry in eList:
        log.trace('AdminConfig.showAttribute(%s, symbolicName)' %(entry), defname)
        name =  AdminConfig.showAttribute(entry, "symbolicName")
        if name == "WAS_INSTALL_ROOT":
            log.trace('AdminConfig.showAttribute(%s, value)' %(entry), defname)
            value = AdminConfig.showAttribute(entry, "value")
            return value
        #end if
    #end for
    #failover
    return getSysEnv('WAS_HOME')
#end getWASHome