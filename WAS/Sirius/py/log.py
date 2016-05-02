'''
Last Update 2016 02 18
@author: sbt-al-gurabi-ia

'''

logLevel = 3# 0-no log, 1-error, 2-warning, 3-info, 4-debug, 5-trace
fulltrace = 0# 0-reduce to 12 chars, 1-full module name

_modules = [
            'java',
            'codecs',
           ]


for module in _modules:
    try:
        locals()[module] = __import__(module, {}, {}, [])
    #end try
    except ImportError:
        print 'Error importing %s.' % module
    #end except
#end for

def error(msg, *args):
  """ Выводит сообщение об ошибке """
  __log(1, 'ERROR', msg, args)

def warn(msg, *args):
  """ Выводит предупреждение """
  __log(2, ' WARN', msg, args)

def info(msg, *args):
  """ Выводит информационное сообщение """
  __log(3, ' INFO', msg, args)

def debug(msg, *args):
  """ Выводит отладочную информацию """
  __log(4, 'DEBUG', msg, args)

def trace(msg, *args):
  """ Выводит подробную информацию """
  __log(5, 'TRACE', msg, args)

def __log(level, prefix, msg, args):
  """ Выводит сообщение на консоль """
  global fulltrace
  if logLevel == 5:
    fulltrace = 1
  #end if
  
  if level <= logLevel:
    if args == None:
      printEcho( '[' + prefix + '] ' + msg, '')
    #end if
    elif len(args)==0:
      printEcho( '[' + prefix + '] ' + msg, 'no defname')
    else:
      printEcho( '[' + prefix + '] ' + msg, args[0])
    #end else
  #end if

def printEcho( message, moduleName):
    if len(message)>1:
        nowtime = curTime("now")
        currenttime = '%-*s' %(19, nowtime)
        totallen=len(moduleName)
        if fulltrace==1:
            currentModule = '%-*s' %(12, moduleName.rjust(12))
        #end if
        elif totallen>12:
            currentModule = '%-*s' %(12, moduleName.rjust(12)[totallen-13:totallen-1])
        #end elif
        else:
            currentModule = '%-*s' %(12, moduleName.rjust(12)[:12])
        #end else
        message_out = "[%s] [%s] **** %s ****" %(currenttime,currentModule,message)
        print message_out
        log2file('write', message_out)
    #end if
#end printEcho
#######

def log2file(execcmd, message):
    from codecs import open
    global defname
    message2file="\n" + message
    log_dir  = getSysEnv('LOG_DIR')
    cur_date = getSysEnv('mydate')
    cur_time = getSysEnv('mytime')
    nowdate = "%s_%s" % (cur_date,cur_time)
    logfilename = getSysEnv('LOG_FILE')
    logfile_path = log_dir + '\\' +logfilename
    if execcmd == "open":
        logfile = codecs.open(logfile_path, 'a','cp1251')
    #end if
    elif execcmd == "write":
        logfile = codecs.open(logfile_path, 'a','cp1251')
        logfile.write(message2file)
        logfile.flush()
    #end elif
    elif execcmd == "close":
        logfile = codecs.open(logfile_path, 'a','cp1251')
        logfile.write(message2file)
        logfile.flush()
        logfile.close()
    #end elif
    else:
        message = "Something went wrong with log file output..."
        print (message)
    #end else
#end log2file

def curTime(execcmd):
    global defname
    currenttime="0000-00-00_00-00-00 UTC"
    from time import gmtime, strftime

    try:
        if execcmd == "date":
            currenttime=strftime("%d %m %Y %H:%M:%S UTC", gmtime())
        #end if
        elif execcmd == "now":
            currenttime=strftime("%Y-%m-%d_%H-%M-%S UTC", gmtime())
        #end elif
        else:
            message="Something went wrong with time..."
            print (message)
        #end else
        return currenttime
    #end try
    except:
        err_message=''
        err_message+="".rjust(37) + str(sys.exc_info()[1])
        message = "Error Occurred on getting current system time.\n%s" %(err_message)    
        print (message)
        pass
    #end except
#end curTime

def getSysEnv(envVarName):
    result=''
    try:
        result = java.lang.System.getenv(envVarName)
    except:
        result = None
    return result
#end getSysEnv

