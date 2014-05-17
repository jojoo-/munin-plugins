#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import subprocess



if 'config' in sys.argv:
    #if we have config specified as commandline option print out the config.

    print """graph_category etckeeper
graph_title Commits to etckeeper
graph_args --base 1000 -l 0
graph_scale no
graph_vlabel Number of Commits
graph_info This graph shows commits to etckeeper.

commit_after_apt.label Commit after APT
commit_after_apt.draw AREA
commit_after_apt.info This means a normal installation

custom_commit.label individualized commit message
custom_commit.draw STACK
custom_commit.info This means the changes were committed manually. Great!

auto_commit.label Autocommitted changes. Shame!
auto_commit.draw STACK
auto_commit.info The changes were checked in by etckeeper either via cron, or before a run of apt. Shame!
"""

else:
    #if we haven't config somewhere in the programm arguments
    
    try:
        log = subprocess.check_output(['git', 'log', 'oneline'], cwd='/etc/')
    except Exception, e:
        print "no git in /etc installed. install it w/ etckeeper"
        sys.exit(1)

    #auto_commit: daily autocommit or 
    #saving uncommitted changes in /etc prior to apt run 
    #-> means etckeeper wasnt invoked manually
    auto_commit = 0

    #committing changes in /etc after apt run
    # -> means config was changed after apt run
    commit_after_apt = 0

    #explicit commit with (hopefully) meaningful message
    custom_commit = 0

    for line in log.splitlines():
        #print line
        if ('daily autocommit' in line) or ('saving uncommitted changes in /etc' in line):
            auto_commit += 1
        elif 'committing changes in /etc after apt run' in line:
            commit_after_apt += 1
        else:
            custom_commit += 1

    print """
commit_after_apt.value {}
custom_commit.value {}
auto_commit.value {}""".format(commit_after_apt, custom_commit, auto_commit)