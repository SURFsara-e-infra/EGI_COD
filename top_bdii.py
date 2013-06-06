#!/usr/bin/env python

import sys,commands,re

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


if __name__=='__main__':
    tmp=psql("select distinct(country) from top_bdii")
    countries=[]
    for i in tmp:
        countries.append(i[0])

    istr="date;"
    for c in countries:
        istr=istr+c+";"
    print istr

    tmp=psql("select distinct(date) from top_bdii order by date asc")
    dates=[]
    for i in tmp:
        dates.append(i[0])

    
    m={}
    for c in countries:
        tmp=psql("select date,availability from top_bdii where country='"+c+"' order by date asc")
        l={}
        for t in tmp:
            l.update({t[0]:t[1]})

        m.update({c:l})
    
    for d in dates:
        s=d+";"
        for c in countries:
            if m.has_key(c):
                if m[c].has_key(d):
                    s=s+str(float(m[c][d]))+";"
                else:
                    s=s+"0.0;"

        print s
