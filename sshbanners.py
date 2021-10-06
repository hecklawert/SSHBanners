#!/usr/bin/env python3
# coding=utf-8

'''

*    @author      Hëck Lawert
*    @githuh      https://github.com/hecklawert
*    @date        25/09/2021
*    @description This tool allows you to connect throught multiple hosts and store the banner into a file. 
*                 Why this tool? Just because.

'''

import sys
import ipaddress
import logging
import socket
import paramiko
import threading, time, random
from queue import Queue
import argparse 

# Global values
public_ranges   = []
jobs            = ''
hostsPathFile   = ''
logPathFile     = ''
parser          = argparse.ArgumentParser()

NORM = '\033[0;37;10m'
BOLD = '\033[1;37;10m'
RED = '\033[1;31;10m'
GREEN = '\033[1;32;10m'
YELLOW = '\033[1;33;10m'
BLUE = '\033[1;34;10m'

BANNER = NORM + '''\

███████╗███████╗██╗  ██╗██████╗  █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ ███████╗
██╔════╝██╔════╝██║  ██║██╔══██╗██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗██╔════╝
███████╗███████╗███████║██████╔╝███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝███████╗
╚════██║╚════██║██╔══██║██╔══██╗██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗╚════██║
███████║███████║██║  ██║██████╔╝██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║███████║
╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝
                                                                                    
''' + NORM + '''
      --== [ by Hëck Lawert] ==--\n'''


# Populate list with public IP CIDR's -- Source: https://www.cidr-report.org/bogons/allocspace-prefix.txt
def generatePublicRanges():
    with open(hostsPathFile) as my_file:
        for line in my_file:
            public_ranges.append(line.strip())
    logging.info('Generated public ranges')

# Scan public ranges in internet
def scanNetwork():
    logging.info('Scanning the internet')
    for range in public_ranges:
        logging.info('Scanning CIDR: '+range)
        subnet = ipaddress.ip_network(range)
        for host in subnet:
            if jobs.qsize() >= 10:
                jobs.join()
            jobs.put(host)
            host = str(host)
            worker = threading.Thread(target=checkHost, args=(host, jobs))
            worker.start()

# Check if we can reach host and get its banner
def checkHost(host, q):
    print(host)
    if isSshOpen(host):
        try:
            c_banner = getBanner(host, '22')
            if c_banner:
                saveBanner(c_banner,host)
        except:
            logging.error('Error on thread') 
            q.get()
            q.task_done()
    q.get()
    q.task_done()

# Check if host has port 22 open            
def isSshOpen(host):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Open socket
    a_socket.settimeout(5)
    location = (host, 22)
    result = a_socket.connect_ex(location) # Check port
    a_socket.close() # Close socket

    # If port is open return true
    if result == 0:
        logging.info(host+' has port 22 open')
        return True
    else:
        return False

# Connect to host to get banner
def getBanner(ip_address, port):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip_address, port=port, username='username', password='bad-password-on-purpose')
    except:
        if not client._transport.get_banner():
            return False
        else:
            return client._transport.get_banner().decode("utf-8")

# Save banner in a file
def saveBanner(banner, host):
    f = open('banners.txt', "a")
    f.write("==============="+host+"===============\n")
    f.write(banner)
    f.close()

# Setup logging configuration
def setLogging(logFilename, debugLevel):
    if debugLevel == 'DEBUG':
        debugLevel = logging.DEBUG
    elif debugLevel == 'INFO':
        debugLevel = logging.INFO
    elif debugLevel == 'WARNING':
        debugLevel = logging.WARNING
    elif debugLevel == 'ERROR':
        debugLevel = logging.ERROR
    elif debugLevel == 'CRITICAL':
        debugLevel = logging.CRITICAL
    else:
        debugLevel = logging.INFO
    logging.basicConfig(filename=logFilename, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s', level=debugLevel)

# Print script instructions
def usage():
    parser.print_help()
    sys.exit(0)

# Parse cmd arguments
def parseCMD():
    # Retrieve global vars
    global hostsPathFile
    global jobs
    global logPathFile

    # read the command-line options
    parser.add_argument("-H", "--hosts", help="Path of a file with hosts in CIDR format")
    parser.add_argument("-c", "--connections", help="Number of simultaneous SSH connections. Default=10", type=int, default=10)
    parser.add_argument("-l", "--log", help="Path of log file", default='SSHBanner.log')
    args = parser.parse_args()

    # if there aren't any options we print the instructions
    if not len(sys.argv[1:]):
        usage()

    # Check arguments
    if args.hosts is not None:
        hostsPathFile = args.hosts
    else:
        print("--hosts argument is required.")
        sys.exit(1)

    # Set arguments
    jobs = Queue(args.connections)
    logPathFile = args.log

def main():
    print(BANNER)
    parseCMD()
    setLogging(logPathFile, 'INFO')
    logging.info('Starting...')
    generatePublicRanges()
    scanNetwork()

if __name__ == "__main__":
    main()
