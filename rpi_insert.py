#!/usr/bin/env python

import sys,re

def main(file,month,year):

    m=re.compile('Asia|Russia|ROC|NGI|CERN')

    f=open(file,'r')
    lines=f.readlines()
    f.close()

    ngi=''
    for line in lines:
        list=line.strip().split(' ')

        if len(list)==4 and m.search(list[0]):
            ngi=list[0]
            alarms_not_handled=list[1]
            expired_tickets=list[2]
            total=list[3]

        date=str(year)+'-'+str(month)+'-'+'1'

        print "insert into rpi (ngi,expired_tickets,alarms_not_handled,total,month,year,date) values ('"+ngi+"',"+str(expired_tickets)+","+str(alarms_not_handled)+","+str(total)+","+str(month)+","+str(year)+",'"+date+"');"
       

if __name__=='__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])
