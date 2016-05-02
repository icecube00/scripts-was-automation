from java.util.regex import Pattern
from WAuJ_utilities import MBnameAsDict, nvTextListAsDict
import java.lang.String as String
import sys


def printUsage():
    print()
    print("Usage: wsadmin -lang jython -f get_log4j_conf_dir.py [wsadmin options] [script options]")
    print()
    print("script options:")
    print("    --help                    - Show this help info")
    print("    --server=<server name>    - WebSphere Server Name. Used in unclustered mode.")


def parseCommandLine(argv):
    fullArgPairPattern = Pattern.compile("--\\w+=\\S*")
    justArgNamePattern = Pattern.compile("--\\w+")
    cmdParamProps = {}
    if (len(argv) > 0):
        for param in argv:
            cmdParam = String(param)
            fullMatcher = fullArgPairPattern.matcher(cmdParam)
            if (fullMatcher.matches()):
                (paramName, paramValue) = cmdParam.split("=")
                cmdParamProps[paramName] = paramValue
            else:
                nameMatcher = justArgNamePattern.matcher(cmdParam)
                if (nameMatcher.matches()):
                    cmdParamProps[param] = None
                else:
                    print("This " + param + " is not a Command Line parameter")
    return cmdParamProps


def getJVMProperties(serverName, parameter):
    jvmProperties = AdminTask.showJVMProperties(["-serverName " + serverName])
    dictJVMProperties = nvTextListAsDict(jvmProperties)
    return dictJVMProperties.get(parameter)


def getNodeName(serverName):
    sBean = AdminControl.completeObjectName("WebSphere:name=" + serverName + ",*")
    sDict = MBnameAsDict(sBean)
    return sDict.get("node")


def getValueOfWSVariable(scope, text):
    if text.count("${") == text.count("}") >= 1:
        firstIndex = text.find("${")
        lastIndex = text.find("}") + 1
        variable = text[firstIndex:lastIndex]
        value = AdminTask.showVariables("[-variableName " + variable[2:-1] + " -scope " + scope + "]")
        text = text.replace(variable, value)
        return getValueOfWSVariable(scope, text.replace(variable, value))
    else:
        return text


# get program arguments
cmdLineParams = parseCommandLine(sys.argv)
if cmdLineParams.get("--server"):
    server = cmdLineParams["--server"]
    # get generic JVM Arguments
    jvmArgs = getJVMProperties(server, "genericJvmArguments")
    if jvmArgs.find("-Dsirius.log4j2.dir") >= 0:
        # find settings with directory for log4j properties
        for arg in jvmArgs[1:-1].split(" -"):
            if arg.find("Dsirius.log4j2.dir") >= 0:
                # get value
                opt, val = arg.split("=", 1)
                val = val.strip()
                # shape a scope
                scp = "Node=" + getNodeName(server) + " Server=" + server
                # get directory for log4j properties
                directory = getValueOfWSVariable(scp, val)
                # adapted only for Windows
                directory = directory.replace("/", "\\")
                print("Target directory: " + directory)
                # write directory to file, because another tips may not work
                f = open("_.temp", "w")
                f.write(directory)
                f.close()
    else:
        print("Argument <-Dsirius.log4j2.dir> not found on a server " + server)
else:
    printUsage()
