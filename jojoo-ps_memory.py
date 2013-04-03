#!/usr/bin/env python
import sys
if len(sys.argv) == 2 and sys.argv[1] == "autoconf":
  print "no"
elif len(sys.argv) == 2 and sys.argv[1] == "config":
  print 'graph_title RSS '
  print 'graph_vlabel Resident Set Size Memory'
  print 'graph_category processes'
  #print 

else:
  from psutil import Process, process_iter, AccessDenied
  from os import environ

  
  proclist= environ.get('names', 'init').split(' ')
  result = {}
  #proclist = ("TextMate", "Chrome", "taskgated", )

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
