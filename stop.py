from subprocess import getstatusoutput

params = [
    "app:app",
    "sougou_cookie.py",
]
comms = ["""ps -ef | grep %s | grep -v grep | awk '{print $2}'""" % param for param in params]

pids = []
for comm in comms:
    ret, opt = getstatusoutput(comm)
    if ret == 0:
        if '\n' not in opt:
            pids.append(opt)
        else:
            pids.extend(opt.split('\n'))

kill_pid_comm = "kill -9 {}"
kill_pid_commands = [kill_pid_comm.format(pid) for pid in pids]

print ("stopping services...")
for comm in kill_pid_commands:
    ret, opt = getstatusoutput(comm)
    if ret == 0:
        print ("{} success".format(comm))
    else:
        print ("{} failed".format(comm))
print ("service stop success")