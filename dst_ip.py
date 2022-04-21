#!/usr/bin/env python3

import re
import xml.dom.minidom
import tempfile
import os,sys
from abc import abstractmethod
import logging
import socket
import traceback
from pathlib import Path
import stat

sys.path.append('/opt/phoenix/data-definition/remediations')

# create IP list html file with appropriate access rights

bashCommand = "chmod +x " + os.path.realpath(__file__)
print(bashCommand)
os.system(bashCommand)
bashCommand = "chown admin " + os.path.realpath(__file__)
os.system(bashCommand)
bashCommand = "chgrp admin " + os.path.realpath(__file__)
os.system(bashCommand)



list_file_name=(Path(__file__).stem)+".html"
print (list_file_name)
listpathandname="/var/www/html/"+list_file_name
listpath=Path(listpathandname)
if listpath.is_file():
    print ('Existing list file')

else:
    print ('No list file')
    print (listpathandname)
    f=open (listpathandname,'w')
    f.write("\n")
    f.close()

bashCommand = "chown admin " + listpathandname
os.system(bashCommand)
bashCommand = "chgrp admin " + listpathandname
os.system(bashCommand)


##################

class Remediation:
    def __init__(self):
        self.tmpFileList = []
        self.log = Logger(os.path.basename(sys.argv[0])[:-3])
        pass

    def __del__(self):
        for tmpFile in self.tmpFileList:
            if os.path.isfile(tmpFile):
                os.remove(tmpFile)
        pass

    def check_usage(self, args):
        if len(args) != 2 and len(args) != len(self.get_arg_list()) + 2:
            print ('Usage: %s incident.xml %s' % (args[0], self.get_arg_list()))
            exit(1)

    @abstractmethod
    def get_arg_list(self):
        print ('Cannot run Base.get_arg_list')
        raise NotImplementedError

    @abstractmethod
    def parse_args(self, args):
        print ('Cannot run Base.parse_args')
        raise NotImplementedError


    @abstractmethod
    def run_remediation(self, args):
        print ('Cannot run Base.run_remediation')
        raise NotImplementedError

    def execute(self, args):
        self.check_usage(args)
        if 2 == len(args):
            self.detect_enforce_on(args[1])
        else:
            self.parse_args(args)
            self.run_remediation(args)

    @staticmethod
    def get_incident_attribute(incident_xml, incident_tag, attr_name):
        doc = xml.dom.minidom.parse(incident_xml)

        nodes = doc.getElementsByTagName(incident_tag)
        if nodes.length < 1:
            print ("Cannot find xml element %s" % incident_tag)
            return None
        else:
            target = nodes[0]
        for node in target.childNodes:
            if node.nodeType == node.ELEMENT_NODE:
                if node.getAttribute("attribute") == attr_name:
                    if node.firstChild:
                        return node.firstChild.data.strip().replace('\r', '').replace('\n', '')
                    else:
                        return None

    @staticmethod
    def get_incident_node_text(incident_xml, incident_tag, attr_name=None, attr_val=None):
        ''' find the 1st node's text, whose attr_name = attr_val '''
        doc = xml.dom.minidom.parse(incident_xml)

        nodes = doc.getElementsByTagName(incident_tag)
        if nodes.length < 1:
            print ("Cannot find xml element %s" % incident_tag)
            return None

        for node in nodes:
            if not attr_name or node.getAttribute(attr_name) == attr_val:
                # found
                for child in node.childNodes:
                    if child.nodeType == child.TEXT_NODE:
                        return child.nodeValue.strip().replace('\r', '').replace('\n', '')

        print ('Cannot find xml element %s, whose attribute %s = %s' % (incident_tag, attr_name, attr_val))

    # enforce on FSM itsealf (extracting destination IP address from incident file and add it to the .html file list)
    def detect_enforce_on(self, incident_xml):
        destIpAddr=self.get_incident_attribute(incident_xml,"incidentTarget", "destIpAddr")
        if destIpAddr is None or destIpAddr == "":
               print ("no incident destination IP Address found!")
               exit(1)
        destIpAddr = re.sub(r'\(.+\)', '', destIpAddr)
        print (destIpAddr)

        #check if IP is already in the file:
        f = open(listpathandname, "r")
        flag = 0
        index = 0
        for line in f:
            index += 1
            if destIpAddr in line:
                flag = 1
                break
        if flag == 0:
            print('Destination IP address', destIpAddr, 'Not Found')
            f = open(listpathandname, "a")
            f.write(destIpAddr)
            f.write("\n")
            f.close()
        else:
            print('IP address', destIpAddr, 'Found In List', index)
        f.close()

    def create_temp_file(self):
        tmpFileObj = tempfile.NamedTemporaryFile(dir="/opt/phoenix/cache/tmp", delete=False, prefix="remediation_")
        self.tmpFileList.append(tmpFileObj.name)
        return tmpFileObj.name

def Logger(name, level=logging.INFO, formatter=None, stdoutStream=True):
    """ Usage:
        log = Logger(name)
        log = Logger(name, logging.DEBUG)
    """
    log = logging.getLogger(name)
    log.setLevel(level)
    hdlr = logging.FileHandler('/tmp/%s.log' % name)
    formatter = logging.Formatter(formatter or '%(asctime)s[%(levelname)s]%(filename)s:%(lineno)d(%(funcName)s) %(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    if stdoutStream == True:
        streamHdlr = logging.StreamHandler()
        streamHdlr.setLevel(logging.ERROR)
        streamFormatter = logging.Formatter('%(levelname)s: %(message)s')
        streamHdlr.setFormatter(streamFormatter)
        log.addHandler(streamHdlr)
    return log


def is_valid_ipv6_address(address):
  try:
    socket.inet_pton(socket.AF_INET6, address)
  except socket.error:  # not a valid address
    return False
  return True

# Check whether the ip is internal ip
def ip_into_int(ip):
    return reduce(lambda x,y:(x<<8)+y,map(int,ip.split('.')))

def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c


class Publish_IP(Remediation):
   def run_remediation(self):
        destIpAddr=self.get_incident_attribute(incident_xml,"incidentTarget", "destIpAddr")
        if destIpAddr is None or destIpAddr == "":
               print ("no incident Destination IP Address found!")
               exit(1)
        destIpAddr = re.sub(r'\(.+\)', '', destIpAddr)
        print (destIpAddr)


if __name__ == "__main__":
    remediation = Publish_IP()
    remediation.execute(sys.argv)
