#!/usr/bin/env python

import sys,re
import pycurl
import StringIO
import getpass
from lxml import etree

key='.globus/userkey.pem'
cert='.globus/usercert.pem'
threshold=70

def get_certified_sites(passwd):

    url='https://goc.egi.eu/gocdbpi/private/?method=get_cert_status_date&certification_status=Certified'
    b=StringIO.StringIO()

    c=pycurl.Curl()
    c.setopt(pycurl.URL,url)
    c.setopt(pycurl.WRITEFUNCTION,b.write)
    c.setopt(pycurl.SSLKEY,key)
    c.setopt(pycurl.SSLCERT,cert)
    c.setopt(pycurl.SSLKEYPASSWD,passwd)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.perform()

    xmldoc=StringIO.StringIO(b.getvalue())
    sites=[]
    for _,e in etree.iterparse(xmldoc,tag='site'):
        elist=list(e)
        d={}
        for i in elist:
            d.update({i.tag:i.text})
        if d['cert_status']=='Certified': sites.append(d['name'])

    return sites

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

    passwd=getpass.getpass('Enter PEM pass phrase:')
    sites=get_certified_sites(passwd)

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
            av=to_int(list[9].strip().split('%')[0])
            rel=to_int(list[10].strip().split('%')[0])
            avm1=to_int(list[13].strip().split('%')[0])
            avm2=to_int(list[14].strip().split('%')[0])

        if site!='' and ngi!='':
            if av<threshold and avm1<threshold and avm2<threshold and site in sites:
                print ngi+";"+site+";"+str(av)+"%;"+str(rel)+"%"
       

if __name__=='__main__':
    main(sys.argv[1])
