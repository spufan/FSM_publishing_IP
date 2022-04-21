#!/usr/bin/python
# -*- encoding: iso-8859-1 -*-

from email import message
from ipaddress import IPv4Address
import socket
import argparse
import os
#from pathlib import Path

FACILITY = {
    'kern': 0, 'user': 1, 'mail': 2, 'daemon': 3,
    'auth': 4, 'syslog': 5, 'lpr': 6, 'news': 7,
    'uucp': 8, 'cron': 9, 'authpriv': 10, 'ftp': 11,
    'local0': 16, 'local1': 17, 'local2': 18, 'local3': 19,
    'local4': 20, 'local5': 21, 'local6': 22, 'local7': 23,
}

LEVEL = {
    'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
    'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}

#folder_path=os.path.realpath(__file__)
folder_path=os.getcwd()
file_syslog=folder_path+'/syslog_msg.txt'
file_log = open(file_syslog, 'r')

#Using for loop
print("Using for loop")


for line in file_log:
    #print("{}".format(line.strip()))
    #syslogmsg=file1.readline()
    #print(file1.readline())
    syslog_msg=line.rstrip()
    print(syslog_msg)

    def syslog(message=syslog_msg, level=LEVEL['notice'], facility=FACILITY['daemon'],
        host="192.168.0.25", port=514, ):
        """
        Send syslog UDP packet to given host and port.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = '%s' % (message)
        #message = '<%d>%s' % (level + facility*8, message)
        sock.connect((host,port))
        sock.sendto(message.encode('utf-8'), (host, port))
        sock.close()

# change 192.168.0.25 with your FortiSIEM local IP address
    syslog(message=syslog_msg,level=1,host="192.168.0.25",port=514)
    #write data to different file
    #file_block_ip.write(syslog_msg)
    #file_block_ip.write("\n")


#Closing files
file_log.close()
#file_block_ip.close()