#!/usr/bin/env python

import sys

ddict={'JAN':'01', \
       'FEB':'02', \
       'MAR':'03', \
       'APR':'04', \
       'MAY':'05', \
       'JUN':'06', \
       'JUL':'07', \
       'AUG':'08', \
       'SEP':'09', \
       'OCT':'10', \
       'NOV':'11', \
       'DEC':'12'}

f=open(sys.argv[1],'r')
list=f.readlines()
f.close()

for line in list:
    record=line.strip().split(';')
    site=record[0]
    tmpdate=record[1].split(' ')[0]
    oldstatus=record[2]
    newstatus=record[3]
    changed_by=record[4]
    comment=record[5]

    tmpdatelist=tmpdate.split('-')
    day=tmpdatelist[0]
    month=ddict[tmpdatelist[1]]
    year=tmpdatelist[2]

    print "insert into status_changes (site,date,old_status,new_status,changed_by,comment) values('"+site+"','"+year+"-"+month+"-"+day+"','"+oldstatus+"','"+newstatus+"','"+changed_by+"','"+comment+"');"
