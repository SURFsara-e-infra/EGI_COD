#!/usr/bin/python

import pycurl
import StringIO
import getpass
import sys
from lxml import etree

key='.globus/userkey.pem'
cert='.globus/usercert.pem'

def get_state_changes(startdate,enddate,passwd):

    url='https://goc.egi.eu/gocdbpi/private/?method=get_cert_status_changes&startdate='+startdate+'&enddate='+enddate
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

    return b.getvalue()

if __name__ == '__main__':

    passwd=getpass.getpass('Enter PEM pass phrase:')
    s=raw_input('Start date <YYYY-MM-DD>:')
    e=raw_input('End date <YYYY-MM-DD>:')
    
    xmldoc=StringIO.StringIO(get_state_changes(s,e,passwd))

    print "SITE;TIME;OLD_STATUS;NEW_STATUS;CHANGED_BY;COMMENT;"
    for _,e in etree.iterparse(xmldoc,tag='result'):
        elist=list(e)
        d={}
        for i in elist:
            d.update({i.tag:i.text})
        if d['COMMENT']==None: d['COMMENT']=''
        print d['SITE']+";"+d['TIME']+";"+d['OLD_STATUS']+";"+d['NEW_STATUS']+";"+d['CHANGED_BY']+";"+d['COMMENT']+";"
