#!/usr/bin/env python
#coding:utf-8

import os,string,sys
import shlex,subprocess
import ConfigParser
import logging
import tarfile,time
from os import path
from optparse import OptionParser

logPath = "/tmp/SetSysEnv.log"

SUGGESTED_MIN_FREE_KBYTES = 4096
MAX_MIN_FREE_KBYTES = 4194304
REQUIRED_OPEN_FILE_LIMIT  = 655360
REQUIRED_PENDING_SIGNALS = "unlimited"
REQUIRED_MAX_USER_PROCESSES = "unlimited"

class InstallError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

def InitOptions():
    execFile = path.basename( sys.argv[0])
    parser = OptionParser()
    parser.disable_interspersed_args()
    parser.add_option("-c","--cgroup", action="store_true", dest="cgroup", help="resource management: control groups config,default: no configuration", default=False)
    parser.add_option("--installPrefix", dest="installPrefix", default="",help="installation directory for cluster logs which are archived on schedule")
    parser.add_option("--dbaUser", dest="dbaUser", default="",help="dba user")
    parser.add_option("--ZTE", action="store_true", dest="z_system_parameters", default=False,help="Do not modify ZTE environment system parameters")
    (options, argv) = parser.parse_args()
    if len( argv ) > 0:
        raise FulltextError("Wrong parameter: %s" % argv)
    return options

def CheckOptions(options):

    logrotate = True
    if len(options.dbaUser) == 0:
        print "\"--dbaUser\" must be assigned."
        sys.exit(1)
    if len(options.installPrefix) == 0:
        print "\"--installPrefix\" must be assigned."
        sys.exit(1)
        
def InitLog(logPath):
    global logger
    logging.raiseExceptions=0
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s %(message)s')
    handler = logging.FileHandler(logPath)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.NOTSET)
    return logger

def ExecCMD(cmd):
    args = shlex.split(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell = True)
    [rv, out, err] = [p.wait(), p.stdout.read(), p.stderr.read()]
    if rv:
        logger.error(out)
        logger.error(err)
    return [rv, out, err]

def CheckExecUser():
    [rv, out, err] = ExecCMD("id -nu")
    if(rv):
        raise InstallError(err)
    curUserName = out.strip()
    if curUserName != "root":
        print("please exec SetSysEnv.py by root, but current user is %s" % curUserName)
        exit(-1)

def CheckDBAUser():
    [rv, out, err] = ExecCMD("id -nu %s"% dbaUser)
    if(rv):
        print("Check DBA user failed: %s" % err)
        exit(-1)

def SetSysctl():
    logger.info("Set kernal parameters...")
    tmpSysctl = '/tmp/tmpSysctl.conf'
    sysctl = '/etc/sysctl.conf'

    try:
        os.system("echo '[test111]' > /tmp/tmpSysctl.conf")
        os.system("cat /etc/sysctl.conf >> /tmp/tmpSysctl.conf")

        cf = ConfigParser.ConfigParser()
        frobj = open(tmpSysctl, 'r')
        cf.readfp(frobj)
        frobj.close()
    except Exception, err:
        logger.error(err)
        raise InstallError(str(err))
    if not options.z_system_parameters:
        cf.set("test111","net.ipv4.tcp_fin_timeout", "1")
        cf.set("test111","net.ipv4.tcp_max_orphans", "3276800")
        cf.set("test111","net.ipv4.tcp_max_tw_buckets", "20000")
        cf.set("test111","net.ipv4.tcp_mem", "94500000 915000000 927000000")
        cf.set("test111","net.ipv4.tcp_timestamps", "0")
        cf.set("test111","net.ipv4.tcp_tw_recycle", "1")
        cf.set("test111","net.ipv4.tcp_tw_reuse", "1")
        
    cf.set("test111","kernel.core_uses_pid", "1")
    cf.set("test111","net.core.netdev_max_backlog", "262144")
    cf.set("test111","net.core.rmem_default", "8388608")
    cf.set("test111","net.core.rmem_max", "16777216")
    cf.set("test111","net.core.somaxconn", "32767")
    cf.set("test111","net.core.wmem_default", "8388608")
    cf.set("test111","net.core.wmem_max", "16777216")
    cf.set("test111","net.ipv4.tcp_max_syn_backlog", "262144")
    cf.set("test111","net.ipv4.tcp_rmem", "4096 87380 4194304")
    cf.set("test111","net.ipv4.tcp_sack", "1")
    cf.set("test111","net.ipv4.ip_local_reserved_ports", "5050,5258,5288,6666,6268")
    cf.set("test111","net.ipv4.tcp_syncookies", "1")
    cf.set("test111","net.ipv4.tcp_window_scaling", "1")
    cf.set("test111","net.ipv4.tcp_wmem", "4096 16384 4194304")
  #  cf.set("test111","vm.min_free_kbytes", str(SUGGESTED_MIN_FREE_KBYTES))
    cf.set("test111","vm.vfs_cache_pressure", "1024")
    cf.set("test111","vm.swappiness", "1")
    cf.set("test111","vm.overcommit_memory", "0")
    cf.set("test111","vm.zone_reclaim_mode", "0")
    try:
        fwobj = open(tmpSysctl, 'w')
        cf.write(fwobj)
        fwobj.close()

        frobj = open(tmpSysctl, 'r')
        tmpSysctlLines = frobj.readlines()
        frobj.close()
        fwobj = open(sysctl, 'w')
        fwobj.writelines(tmpSysctlLines[1:-1])
        logger.info(tmpSysctlLines[1:-1])
        fwobj.close()

    except Exception, err:
        logger.error(err)
        raise InstallError(str(err))

    cmd = "/sbin/sysctl -p"
    logger.info(cmd)
    [rv, out, err] = ExecCMD(cmd)
    if(rv):
        logger.error(err)
    ExecCMD("rm -f %s" % tmpSysctl)
    logger.info("Set kernal parameters to end.")

def SetSecurityLimits():
    logger.info("Set system open files...")
    logger.info("reference: ulimit -n, value: 655360")
    #checkCmds = "[ `ulimit -n` == 655360 ]"
    #logger.info("exec cmd:%s" % checkCmds)
    #rc = os.system(checkCmds)
    #if rc == 0:
    #    logger.info("exec cmd:%s, return value: 655360" % checkCmds)
    cmds = []
    if path.exists("/etc/security/limits.conf"):
        #cmds.append(r"sed -i.bck -e 's/^\(\*\s*\)\(soft\|hard\)\(\s\+nofile\)/#Commented out by gcluster\n#\1\2\3/g' /etc/security/limits.conf")
        cmds.append(r"sed -i.bck -e 's/^\(%s\s*\)\(soft\|hard\)\(\s\+nofile\)/#Commented out by gcluster\n#\1\2\3/g' /etc/security/limits.conf " % dbaUser)
        #cmds.append(r"sed -i.bck -e 's/^\(\*\s*\)\(soft\|hard\)\(\s\+nproc\)/#Commented out by gcluster\n#\1\2\3/g' /etc/security/limits.conf ")
        cmds.append(r"sed -i.bck -e 's/^\(%s\s*\)\(soft\|hard\)\(\s\+nproc\)/#Commented out by gcluster\n#\1\2\3/g' /etc/security/limits.conf " % dbaUser)
        #cmds.append(r"sed -i.bck -e 's/^\(\*\s*\)\(soft\|hard\)\(\s\+sigpending\)/#Commented out by gcluster\n#\1\2\3/g' /etc/security/limits.conf ")
        cmds.append(r"sed -i.bck -e 's/^\(%s\s*\)\(soft\|hard\)\(\s\+sigpending\)/#Commented out by gcluster\n#\1\2\3/g' /etc/security/limits.conf " % dbaUser)
        cmds.append(r"sed -i -e 's/^# End of file/#/g' /etc/security/limits.conf ")
        cmds.append("/bin/bash -c \"echo -e '# Added by gcluster\\n%s\\tsoft\\tnofile\\t%d' >>/etc/security/limits.conf\"" % (dbaUser,REQUIRED_OPEN_FILE_LIMIT))
        cmds.append("/bin/bash -c \"echo -e '# Added by gcluster\\n%s\\thard\\tnofile\\t%d' >>/etc/security/limits.conf\"" % (dbaUser,REQUIRED_OPEN_FILE_LIMIT))
        if not options.z_system_parameters:
            cmds.append("/bin/bash -c \"echo -e '# Added by gcluster\\n%s\\tsoft\\tsigpending\\t%s' >>/etc/security/limits.conf\""% (dbaUser,REQUIRED_PENDING_SIGNALS))
            cmds.append("/bin/bash -c \"echo -e '# Added by gcluster\\n%s\\thard\\tsigpending\\t%s' >>/etc/security/limits.conf\""% (dbaUser,REQUIRED_PENDING_SIGNALS))
            cmds.append("/bin/bash -c \"echo -e '# Added by gcluster\\n%s\\tsoft\\tnproc\\t%s' >>/etc/security/limits.conf\"" % (dbaUser,REQUIRED_MAX_USER_PROCESSES))
            cmds.append("/bin/bash -c \"echo -e '# Added by gcluster\\n%s\\thard\\tnproc\\t%s' >>/etc/security/limits.conf\""% (dbaUser,REQUIRED_MAX_USER_PROCESSES)) 
        cmds.append("/bin/bash -c \"echo -e '# End of file' >>/etc/security/limits.conf\"")

        cmds.append("/bin/bash -c \"if [ -f /etc/pam.d/su ]; then if [ `egrep '^[[:space:]]*session[[:space:]]+required[[:space:]]+pam_limits\.so' /etc/pam.d/su |\
                wc -l` -eq 0 ]; then echo 'session required pam_limits.so' >> /etc/pam.d/su;  fi fi\"")
        #cmds.append(r'sed -i "s/\(^\*\s*soft\s*nproc.*\)/#\1/g" /etc/security/limits.d/*-nproc.conf')
        [rv,out,err] = ExecCMD("stat /etc/security/limits.d/*-nproc.conf --format=%n")
        if not rv:
            cmds.append(r'sed -i "s/\(^\*\s*soft\s*nproc.*\)/#\1/g" /etc/security/limits.d/*-nproc.conf')
        #add for suse 11 SP1 SP2 SP3
        if path.exists("/etc/sysconfig/ulimit"):
            cmds.append(r'sed -i "s/\(^HARDFDLIMIT.*\)/\(HARDFDLIMIT=\"%d\"\)/g" /etc/sysconfig/ulimit' % REQUIRED_OPEN_FILE_LIMIT)
            cmds.append(r'sed -i "s/\(^SOFTFDLIMIT.*\)/\(SOFTFDLIMIT=\"%d\"\)/g" /etc/sysconfig/ulimit' % REQUIRED_OPEN_FILE_LIMIT)

        for cmd in cmds:
            [rv, out, err] = ExecCMD(cmd)
            if(rv):
                logger.error(err)
                raise InstallError(str(err))
            else:
                logger.info(cmd)
    logger.info("Set system open files to end.")

def SetFileSizeLimit():
    logger.info("Set system file size...")
    logger.info("reference: ulimit -f, value: unlimited")
    checkCmds = '[ `ulimit -f` == \"unlimited\" ]'
    logger.info("exec cmd:%s" % checkCmds)
    rc = os.system(checkCmds)
    cmds = []
    if rc == 0:
        logger.info("exec cmd:%s, return value: unlimited" % checkCmds)
    if(rc != 0 and path.exists("/etc/security/limits.conf")):
        cmds.append(r"sed -i.bck -e 's/^\(\*\s*\)\(soft\|hard\)\(\s\+fsize\)/#Commented out by gcluster\n#\1\2\3/g' /etc/security/limits.conf")
        cmds.append(r"sed -i -e 's/^# End of file/#/g' /etc/security/limits.conf ")
        cmds.append("/bin/bash -c \"echo -e '# Added by gcluster\\n%s\\tsoft\\tfsize\\tunlimited' >>/etc/security/limits.conf\""% dbaUser)
        cmds.append("/bin/bash -c \"echo -e '# Added by gcluster\\n%s\\thard\\tfsize\\tunlimited' >>/etc/security/limits.conf\""% dbaUser)
        cmds.append("/bin/bash -c \"echo -e '# End of file' >>/etc/security/limits.conf\"")

        for cmd in cmds:
            [rv, out, err] = ExecCMD(cmd)
            if(rv):
                logger.error(err)
                raise InstallError(str(err))
            else:
                logger.info(cmd)
    logger.info("Set system file size to end.")

def SetFileMax():
    logger.info("Set system kernal parameter 'file max'...")
    checkCmd = """/bin/bash -c \"
            suggested_file_max=`grep MemTotal /proc/meminfo | awk '{printf \"%.0f\",$2/1024}'`;
            current_file_max=`cat /proc/sys/fs/file-max`;
            if [ $? -eq 0 ];
            then
                if [ \$suggested_file_max -lt 65536 ];
                then
                    suggested_file_max=65536;
                fi;
                if [ $? -eq 0 ];
                then
                    if [ \$current_file_max -ge \$suggested_file_max ];
                    then
                        echo 0;
                    else
                        echo \$suggested_file_max;
                    fi;
                fi;
            fi;\""""
    robj = os.popen(checkCmd)
    rc = robj.readline().strip()
    robj.close()
    res = int(rc)
    if(res > 0):
        cmds = []
        cmds.append("/sbin/sysctl -w fs.file-max=%d" % res)
        cmds.append(r"sed -i.bck -e 's/^\(\s*fs\.file-max\)/#Commented out by gcluster\n#\1/g' /etc/sysctl.conf ")
        cmds.append("/bin/bash -c \"echo '# Added by gcluster' >> /etc/sysctl.conf\"")
        cmds.append("/bin/bash -c \"echo 'fs.file-max = %d' >> /etc/sysctl.conf\"" % res)
        for cmd in cmds:
            [rv, out, err] = ExecCMD(cmd)
            if(rv):
                logger.error(err)
                raise InstallError(str(err))
            else:
                logger.info(cmd)
    logger.info("Set system kernal parameter 'file max' to end.")

def SetMaxMapCount():
    logger.info("Set system kernal parameter 'max_map_count'...")
    checkCmds = """/bin/bash -c \"
                    suggested_max_map=`grep MemTotal /proc/meminfo | awk '{printf \"%.0f\",$2/16}'`;
                    current_max_map=`cat /proc/sys/vm/max_map_count`;
                    if [ $? -eq 0 ];
                    then
                        if [ \$current_max_map -ge \$suggested_max_map ];
                        then
                            echo 0;
                        else
                            echo \$suggested_max_map;
                        fi;
                    fi;\"""";
    robj = os.popen(checkCmds)
    rc = robj.readline().strip()
    robj.close()
    res = int(rc)
    if(res > 0):
        cmds = []
        cmds.append("/sbin/sysctl -w vm.max_map_count=%d" % res)
        cmds.append(r"sed -i.bck -e 's/^\(\s*vm\.max_map_count\)/#Commented out by gcluster\n#\1/g' /etc/sysctl.conf ")
        cmds.append("/bin/bash -c \"echo '# Added by gcluster' >> /etc/sysctl.conf\"")
        cmds.append("/bin/bash -c \"echo 'vm.max_map_count = %d' >> /etc/sysctl.conf\"" % res)
        for cmd in cmds:
            [rv, out, err] = ExecCMD(cmd)
            if(rv):
                logger.error(err)
                raise InstallError(str(err))
            else:
                logger.info(cmd)
    logger.info("Set system kernal parameter 'max_map_count' to end.")

def SetMinFreeKbytes():
    logger.info("Set system kernal parameter 'min_free_kbytes'...")
    sgValue = None
    cmd = '''echo "`grep MemTotal /proc/meminfo | awk '{printf "%.0f",$2}'`/10" | bc'''
    [rv, out, err] = ExecCMD(cmd)
    if(0 == rv):
        sgValue = out.strip()
        if int(sgValue) > MAX_MIN_FREE_KBYTES:
            sgValue=str(MAX_MIN_FREE_KBYTES)
    else:
        strErr = "Fail to exec %s, reason: %s" % (cmd, str(err))
        logger.error(strErr)
        raise InstallError(strErr)
    if(sgValue):
        cmds = []
        cmds.append(r"/sbin/sysctl -w vm.min_free_kbytes=%s" % sgValue)
        cmds.append(r"sed -i.bck -e 's/^\(\s*vm\.min_free_kbytes.*\)/#\1 #Commented out by gcluster/g' /etc/sysctl.conf")
        cmds.append(r"echo vm\.min_free_kbytes = %s >> /etc/sysctl.conf" % sgValue)
        for cmd in cmds:
            [rv, out, err] = ExecCMD(cmd)
            if rv:
                strErr = "Fail to set vm.min_free_kbytes, cmd: %s, reason: %s" % (cmd, err)
                logger.error(strErr)
                raise InstallError(strErr)
            else:
                logger.info(cmd)
    logger.info("Set system kernal parameter 'min_free_kbytes' to end.")

def SetMaxMemSize():
    logger.info("Set system max memory size...")
    logger.info("reference: ulimit -m, value: unlimited")
    value = None
    cmd = 'su - %s -c "ulimit -m"' % dbaUser
    logger.info("exec cmd:%s" % cmd)
    [rv, out, err] = ExecCMD(cmd)
    if(0 == rv):
        value = out.strip()
    else:
        logger.error("Fail to exec: %s" % cmd)
        raise InstallError(err)
    logger.info("exec cmd:%s,and return value:%s" % (cmd,value))
    if(value != 'unlimited'):
        cmds = []
        cmds.append(r"ulimit -m unlimited")
        cmds.append(r"sed -i.bck -e 's/^\(%s\s.*soft.*rss.*\)/#\1 #Commented out by gcluster/g' /etc/security/limits.conf" % dbaUser)
        cmds.append(r"sed -i.bck -e 's/^\(%s\s.*hard.*rss.*\)/#\1 #Commented out by gcluster/g' /etc/security/limits.conf" % dbaUser)
        cmds.append(r"echo '%s        soft    rss        unlimited' >> /etc/security/limits.conf" % dbaUser)
        cmds.append(r"echo '%s        hard    rss        unlimited' >> /etc/security/limits.conf" % dbaUser)
        for cmd in cmds:
            [rv, out, err] = ExecCMD(cmd)
            if rv:
                strErr = "Fail to set max memory size, cmd: %s, reason: %s" % (cmd, err)
                logger.error(strErr)
                raise InstallError(strErr)
            else:
                logger.info(cmd)
    logger.info("Set system max memory size to end.")

def SetVitualMem():
    logger.info("Set system virtual memory...")
    logger.info("reference: ulimit -v, value: unlimited")
    value = None
    cmd = 'su - %s -c "ulimit -v"' % dbaUser
    logger.info("exec cmd:%s" % cmd)
    [rv, out, err] = ExecCMD(cmd)
    if(0 == rv):
        value = out.strip()
    else:
        logger.error("Fail to exec: %s" % cmd)
        raise InstallError(err)
    logger.info("exec cmd:%s,and return value:%s" % (cmd,value))
    if(value != 'unlimited' and path.exists("/etc/security/limits.conf")):
        cmds = []
        cmds.append(r"ulimit -v unlimited")
        cmds.append(r"sed -i.bck -e 's/^\(%s\s.*soft.*as.*\)/#\1 #Commented out by gcluster/g' /etc/security/limits.conf" % dbaUser)
        cmds.append(r"sed -i.bck -e 's/^\(%s\s.*hard.*as.*\)/#\1 #Commented out by gcluster/g' /etc/security/limits.conf" % dbaUser)
        cmds.append(r"echo '%s        soft    as        unlimited' >> /etc/security/limits.conf" % dbaUser)
        cmds.append(r"echo '%s        hard    as        unlimited' >> /etc/security/limits.conf" % dbaUser)
        for cmd in cmds:
            [rv, out, err] = ExecCMD(cmd)
            if rv:
                strErr = "Fail to set vitual memory, cmd: %s, reason: %s" % (cmd, err)
                logger.error(strErr)
                raise InstallError(strErr)
            else:
                logger.info(cmd)
    logger.info("Set system virtual memory to end")

def SetEnv():
    logger.info("Start modification of system env.")
    SetSysctl()
    SetSecurityLimits()
    SetFileSizeLimit()
    SetFileMax()
    SetMaxMapCount()
    SetMinFreeKbytes()
    SetMaxMemSize()
    SetVitualMem()
    logger.info("Modify system env end.")

def ClearULimitConf():
    limitd = "/etc/security/limits.d"
    if not path.exists(limitd):
        return
    limitConf = ""
    for file in os.listdir(limitd):
        if file.find("ulimits") >= 0:
            limitConf = path.join(limitd,file)
            break
    if len(limitConf) != 0:
        ExecCMD("rm -rf %s" % limitConf)

def GetMultiIpList(prefix):

    hostList = []
    hostPrefixList = []
    cmd = "ls -l %s |grep '^d' | awk  '{print $NF}'"%prefix
    [rv, out, err] = ExecCMD(cmd)
    if(0 == rv):
        value = out.strip()
    else:
        logger.error("Fail to exec: %s" % cmd)
        raise InstallError(err)
    for h in out.split():
        hostList.append(h.strip())
    for TmpPrefix in hostList:
        gbase_profile_path = os.path.exists(os.path.join(prefix,TmpPrefix,"gbase_profile"))
        gcware_profile_path = os.path.exists(os.path.join(prefix,TmpPrefix,"gcware_profile"))
        if gbase_profile_path or gcware_profile_path:
            hostPrefixList.append(TmpPrefix)
    return hostPrefixList


def SetCoLogrotateLogConf():
    
    for hostPrefix in InstallPrefixList:
        logger.info("Start adding configuration information for gcware.log...")
        confPath = "%s/gcware/log/gcware.log" % os.path.join(prefix,hostPrefix)
        if os.path.exists(confPath):
            confFile = "/etc/logrotate.d/gcware_%s"%hostPrefix
            lines = []
            lines.append("%s{" % confPath)
            lines.append("  missingok")
            lines.append("  compress")
            lines.append("  copytruncate")
            lines.append("  daily")
            lines.append("  rotate 31")
            lines.append("  size 10M")
            lines.append("  minsize 1M")
            lines.append("  notifempty")
            lines.append("}")
            try:
                fwobj = open(confFile, 'w')
                fwobj.write(string.join(lines, '\n'))
                logger.info(string.join(lines,'\n'))
                fwobj.close()
            except Exception, err:
                logger.error(str(err))
                raise InstallError(str(err))
            logger.info("add gcware.log configuration information to end.")

def SetGcwareLogConf():

    ExecCMD("rm -rf /etc/logrotate.d/gcware*")
    for hostPrefix in InstallPrefixList:
        confFileDir = "/etc/logrotate.d"
        confFile = "/etc/logrotate.d/gcware_%s"%hostPrefix
        confLog = "%s/gcware/log/gcware.log" % os.path.join(prefix,hostPrefix)
        if path.exists(confFileDir):
            logger.info("Set gcware logrotate log...")
            if not path.exists(confFile):
                SetCoLogrotateLogConf()
            else:
                try:
                    fwobj = open(confFile, 'r')
                    lines = fwobj.readlines()
                    fwobj.close()
                except Exception, err:
                    logger.error(str(err))
                if confLog not in lines[0]:
                    ExecCMD("rm -rf %s" % confFile)
                    SetCoLogrotateLogConf()
                else:
                    logger.info("existing %s, do nothing." % confLog)
            logger.info("Set gcware logrotate log to end.")

def SetGcLogrotateLogConf(logfile,hostPrefix):
    logger.info("Start adding configuration information for %s.log..." % logfile)
    confFile = "/etc/logrotate.d/gc_%s_%s" % (logfile,hostPrefix)
    lines = []
    lines.append("%s/gcluster/log/gcluster/%s.log{" % (path.join(prefix,hostPrefix),logfile))
    lines.append("  missingok")
    lines.append("  compress")
    lines.append("  copytruncate")
    lines.append("  daily")
    lines.append("  rotate 31")
    lines.append("  size 10M")
    lines.append("  minsize 1M")
    lines.append("  notifempty")
    lines.append("}")
    try:
        fwobj = open(confFile, 'w')
        fwobj.write(string.join(lines, '\n'))
        logger.info(string.join(lines,'\n'))
        fwobj.close()
    except Exception, err:
        logger.error(str(err))
        raise InstallError(str(err))
    logger.info("add %s.log configuration information to end." % logfile)

def SetGnLogrotateLogConf(logfile,hostPrefix):
    logger.info("Start adding configuration information for %s.log..." % logfile)
    confFile = "/etc/logrotate.d/gn_%s_%s" % (logfile,hostPrefix)
    lines = []
    lines.append("%s/gnode/log/gbase/%s.log{" % (os.path.join(prefix,hostPrefix),logfile))
    lines.append("  missingok")
    lines.append("  compress")
    lines.append("  copytruncate")
    lines.append("  daily")
    lines.append("  rotate 31")
    lines.append("  size 10M")
    lines.append("  minsize 1M")
    lines.append("  notifempty")
    lines.append("}")
    try:
        fwobj = open(confFile, 'w')
        fwobj.write(string.join(lines, '\n'))
        logger.info(string.join(lines,'\n'))
        fwobj.close()
    except Exception, err:
        logger.error(str(err))
        raise InstallError(str(err))
    logger.info("add %s.log configuration information to end." % logfile)

def SetLogrotateGCLogConf():
    confFileDir = "/etc/logrotate.d"
    if path.exists(confFileDir):
        logger.info("Set gcluster logrotate log...")
        for f in ["express","system","gc_recover","loader_result"]:
            ExecCMD("rm -rf /etc/logrotate.d/gc_%s*" % f)
        for hostPrefix in InstallPrefixList:
            TmpPrefix = os.path.join(prefix,hostPrefix)
            if path.exists("%s/gcluster/log/gcluster" % TmpPrefix): 
                for f in ["express","system","gc_recover","loader_result"]:
                    confLog = "%s/gcluster/log/gcluster/%s.log" % (prefix,f)
                    confFileName = "/etc/logrotate.d/gc_%s_%s" % (f,hostPrefix)
                    if not path.exists(confFileName):
                        SetGcLogrotateLogConf(f,hostPrefix)
                    else:
                        try:
                            fwobj = open(confFileName, 'r')
                            lines = fwobj.readlines()
                            fwobj.close()
                        except Exception, err:
                            logger.error(str(err))
                        if confLog not in lines[0]:
                            ExecCMD("rm -rf %s" % confFileName)
                            SetGcLogrotateLogConf(f,hostPrefix)
                        else:
                            logger.info("existing %s, do nothing." % confLog)
        logger.info("Set gcluster logrotate log to end.")

def SetLogrotateGNLogConf():
    confFileDir = "/etc/logrotate.d"
    if path.exists(confFileDir):
        logger.info("Set gnode logrotate log...")
        for f in ["express","system","syncserver","loader_result"]:
            ExecCMD("rm -rf /etc/logrotate.d/gn_%s*" % f)
        for hostPrefix in InstallPrefixList:
            TmpPrefix = os.path.join(prefix,hostPrefix)
            if path.exists("%s/gnode/log/gbase" % TmpPrefix):
                for f in ["express","system","syncserver","loader_result"]:
                    confLog = "%s/gnode/log/gbase/%s.log" % (TmpPrefix,f)
                    confFileName = "/etc/logrotate.d/gn_%s_%s" % (f,hostPrefix)
                    if not path.exists(confFileName):
                        SetGnLogrotateLogConf(f,hostPrefix)
                    else:
                        try:
                            fwobj = open(confFileName, 'r')
                            lines = fwobj.readlines()
                            fwobj.close()
                        except Exception, err:
                            logger.error(str(err))
                        if confLog not in lines[0]:
                            ExecCMD("rm -rf %s" % confFileName)
                            SetGnLogrotateLogConf(f,hostPrefix)
                        else:
                            logger.info("existing %s, do nothing." % confLog)
        logger.info("Set gnode logrotate log to end.")

def GetCgroupSubSys():
    [rv, out, err] = ExecCMD("lssubsys -a")
    if(not rv):
        return out
    else:
        return ""

def SetCgroupConf():
    if not cgroup:
        return
    logger.info("Set cgroup config file...")
    logger.info("reference: /etc/cgconfig.conf")
    subsys = GetCgroupSubSys()
    try:
        f = open( "/etc/cgconfig.conf", 'w' )
        f.write("#\n");
        f.write("#  Copyright IBM Corporation. 2007\n")
        f.write("#\n")
        f.write("#  Authors:     Balbir Singh <balbir@linux.vnet.ibm.com>\n")
        f.write("#  This program is free software; you can redistribute it and/or modify it\n")
        f.write("#  as published by the Free Software Foundation.\n")
        f.write("#\n")
        f.write("#  This program is distributed in the hope that it would be useful, but\n")
        f.write("#  WITHOUT ANY WARRANTY; without even the implied warranty of\n")
        f.write("#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.\n")
        f.write("#\n")
        f.write("# See man cgconfig.conf for further details.\n")
        f.write("#\n")
        f.write("# By default, mount all controllers to /cgroup/<controller>\n")
        f.write("\n")
        f.write("\n")
        f.write("mount {\n")
        f.write("        cpu     = /cgroup/cpu;\n")
        f.write("        cpuacct = /cgroup/cpuacct;\n")
        if "blkio" in subsys:
            f.write("        blkio   = /cgroup/blkio;\n")
        f.write("        }\n")
        f.write("\n")
        f.write("group gbase {\n")
        f.write("        perm{\n")
        f.write("            task{\n")
        f.write("                uid = %s;\n" % dbaUser)
        f.write("                gid = %s;\n" % dbaUser)
        f.write("                }   \n")
        f.write("            admin{\n")
        f.write("                uid = %s;\n" % dbaUser)
        f.write("                gid = %s;\n" % dbaUser)
        f.write("                }   \n")
        f.write("            }\n")
        f.write("        cpu{\n")
        f.write("            }\n")
        f.write("        cpuacct{\n")
        f.write("            }\n")
        if "blkio" in subsys:
            f.write("        blkio{\n")
            f.write("            }   \n")
        f.write("        }\n")

    except Exception, err:
        logger.error(str(err))
        raise InstallError("Set cgroup config failed: %s" % str(err))
    logger.info("Set cgroup config file to end.")


def IsSupportIPv6():
    if not path.exists("/sbin/sysctl"):
        return
    cmds = []
    cmds.append("/sbin/sysctl net.ipv6.conf.all.disable_ipv6 | awk '{print $3}'")
    cmds.append("/sbin/sysctl net.ipv6.conf.default.disable_ipv6 | awk '{print $3}'") 
    
    isSup = True
    for cmd in cmds:
        [rv,out,err] = ExecCMD(cmd)
        if rv or len(err) != 0:
            isSup = False
            logger.info(err)
        if not rv and len(err) == 0:
            if int(out) != 0:
                isSup = False
    if not isSup: 
        print "warning:IPV6 protocol not supported,if you want to use it,please turn it on..."
            
def main():
    global prefix
    global dbaUser
    global options
    global cgroup
    global InstallPrefixList
    
    options = InitOptions()
    CheckOptions(options)
    CheckExecUser()
    logger = InitLog(logPath)

    prefix = options.installPrefix
    dbaUser = options.dbaUser
    cgroup = options.cgroup
    InstallPrefixList = GetMultiIpList(prefix)

    try:
        CheckDBAUser()
        SetEnv()
        ClearULimitConf()
        SetCgroupConf()
        SetGcwareLogConf()
        SetLogrotateGCLogConf()
        SetLogrotateGNLogConf()
        IsSupportIPv6()
    except InstallError, err:
        res = "Fail to modify system parameters. Reason: %s. Please refer to %s" % (str(err), logPath)
        print res
        sys.exit(1)

if __name__ == '__main__':
    main()
