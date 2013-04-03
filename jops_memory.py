#!/usr/bin/env python
''' munin plugin for multips_memory.
twice as fast as the multips_memory

depends on psutil;
pip install psutil or apt-get install python-psutil

configure in /etc/munin/plugin-conf.d/munin-node
and add for an example
[jops_memory]
env.names amavis slapd named mysqld httpd saslauthd


'''

import sys
from os import environ
proclist= environ.get('names', 'init').split(' ')
if len(sys.argv) == 2 and sys.argv[1] == "autoconf":
  print "no"
elif len(sys.argv) == 2 and sys.argv[1] == "config":
  print 'graph_title RSS '
  print 'graph_vlabel Resident Set Size Memory'
  print 'graph_category processes'
  for i in proclist:
    print "%s.label %s" % (i, i)
  #print 

else:
  from psutil import Process, process_iter, AccessDenied
  result = {}

  # go throu all processes, proc is the process we're examining
  for proc in process_iter():
  
    #go throu all searched processes, searchproc is the process
    #we're examining/searching
    for searchproc in proclist:
   
      #try to use the cmdline parameter, if it is not allowed, use just the name
      try:
        compproc = ' '.join(proc.cmdline) #cmdline is a list, join it with " "
      except (AccessDenied):
        compproc = proc.name
    
      #have we found a matching process?  
      #find returns the position of the fund string or -1
      if (compproc.find(searchproc) > 0):
        #store result in dictionary result
        #first test if we already have a key, else add the value
        if searchproc not in result:
          result[searchproc] = proc.get_memory_info()[1] #1 is rss, 2 is vms
        else:
          result[searchproc] += proc.get_memory_info()[1]


  #after the processing has finnished

  #check if we did'nt find some Processes
  for i in proclist:
    if i not in result:
      result[i] = '-'

  #display processes
  for i in result:
    print "%s.value %s" % (i, result[i])
