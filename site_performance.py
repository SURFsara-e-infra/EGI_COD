#!/usr/bin/env python

import sys,re
import pycurl
import StringIO
import getpass
import commands
import os
from lxml import etree

home=os.getenv("HOME")
key=home+'/.globus/userkey.pem'
cert=home+'/.globus/usercert.pem'
thresholdA=90
thresholdR=95

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

def psql (command):

   ret=commands.getoutput('psql -h localhost -t -c \"'+command+';\"').split('\n')
   list=[]
   for i in ret:
       tmp=i.split('|')
       l=[]
       for j in tmp:
           a=j.strip()
           if a!='':
               l.append(j.strip())

       if len(l)>0: list.append(l)

   return list

def main(date0,date1):

    passwd=getpass.getpass('Enter PEM pass phrase:')
    sites=get_certified_sites(passwd)


    tmp=psql("select site,ngi,count(date) from aru where date>='"+date0+"' and date<='"+date1+"' and (availability<"+str(thresholdA)+" or reliability<"+str(thresholdR)+") group by site,ngi order by count(date) desc;")

    f=open('site_performance.csv','w')
    for r in tmp:
        site=r[0]
        count=r[1]

        if site in sites:
            f.write(site+';'+str(count)+';\n')
    f.close()
        


if __name__=='__main__':

    s=raw_input('Start year-month <YYYY-MM>:')
    e=raw_input('End year-month <YYYY-MM>:')

    date0=s+"-01"
    date1=e+"-01"

    main(date0,date1)
