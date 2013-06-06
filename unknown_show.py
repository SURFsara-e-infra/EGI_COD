#!/usr/bin/env python

import sys,re

def to_int(a):
    try:
        v=int(a)
    except:
        v=-1

    return v

def main(file):

    m=re.compile('Asia|Russia|ROC|NGI|CERN')
    m1=re.compile('AsiaPacific')
    m2=re.compile('Russia')
    m3=re.compile('CERN')

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
    
            if m1.search(ngi): ngi='ROC_Asia/Pacific'
            if m2.search(ngi): ngi='ROC_Russia'
            if m3.search(ngi): ngi='ROC_CERN'
        
        if len(list)==16:
            site=list[3]
            unknown=to_int(list[11].strip().split('%')[0])

        if site!='' and ngi!='':
            if unknown>10:
                print ngi+";"+site+";"+str(unknown)+"%"
       

if __name__=='__main__':
    main(sys.argv[1])
