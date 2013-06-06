#!/usr/bin/env python

import sys,re

def to_int(a):
    try:
        v=int(a)
    except:
        v=-1

    return v

def main(file,month,year):

    m=re.compile('Asia|Russia|ROC|NGI|CERN')

    f=open(file,'r')
    lines=f.readlines()
    f.close()

    ngi=''
    for line in lines:
        list=line.strip().split(',')

        if len(list)!=2 and len(list)!=16 : continue

        if len(list)==2 and m.search(list[0]):
            ngi=list[0]
            site=''
            unknown=''
            pcpus=''
            lcpus=''
            av=''
            rel=''
        
        if len(list)==16:
            site=list[3]
            pcpus=to_int(list[6])
            lcpus=to_int(list[7])
            av=to_int(list[9].strip().split('%')[0])
            rel=to_int(list[10].strip().split('%')[0])
            unknown=to_int(list[11].strip().split('%')[0])

        date=str(year)+'-'+str(month)+'-'+'1'
        if site!='' and ngi!='':
            print "insert into aru (ngi,site,lcpus,pcpus,availability,reliability,unknown,month,year,date) values ('"+ngi+"','"+site+"',"+str(lcpus)+","+str(pcpus)+","+str(av)+","+str(rel)+","+str(unknown)+","+str(month)+","+str(year)+",'"+date+"');"
       

if __name__=='__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])
