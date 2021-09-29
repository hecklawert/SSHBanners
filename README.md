# Description

A fast SSH mass-scanner and banner grabber tool.

# Usage

```
[ heck@workstation ~ ]$ ./sshbanners -h

███████╗███████╗██╗  ██╗██████╗  █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ ███████╗
██╔════╝██╔════╝██║  ██║██╔══██╗██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗██╔════╝
███████╗███████╗███████║██████╔╝███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝███████╗
╚════██║╚════██║██╔══██║██╔══██╗██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗╚════██║
███████║███████║██║  ██║██████╔╝██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║███████║
╚══════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝
                                                                                    

      --== [ by Hëck Lawert] ==--

usage: sshbanners.py [-h] [-H HOSTS] [-c CONNECTIONS] [-l LOG]

optional arguments:
  -h, --help            show this help message and exit
  -H HOSTS, --hosts HOSTS
                        Path of a file with hosts in CIDR format
  -c CONNECTIONS, --connections CONNECTIONS
                        Number of simultaneous SSH connections. Default=10
  -l LOG, --log LOG     Path of log file

```

# Examples

## Simple use

```
[ heck@workstation ~ ]$ ./sshbanners -H hosts.txt
```

## Set SSH simultaneous connections and log path

```
[ heck@workstation ~ ]$ ./sshbanners -H hosts.txt -c 10 -l /var/sys/log/sshbanner.log
```

# Author

Hëck Lawert

# Notes

- quick'n'dirty code

# License

Check docs/LICENSE.

# Disclaimer
Use with educational purposes.
