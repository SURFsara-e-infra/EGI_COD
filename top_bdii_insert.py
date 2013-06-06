#!/usr/bin/env python

import sys,re

def to_float(a):
    try:
        v=float(a)
    except:
        v=-1.0

    return v

def main(file,month,year):


   f=open(file,'r')
   lines=f.readlines()
   f.close()

   avd={}
   reld={}
   dav={}
   drel={}
   c={}

   for line in lines[6:]:
       list=line.strip().split(';')

       country=list[1]
       av=to_float(list[3].strip().split('%')[0])
       rel=to_float(list[4].strip().split('%')[0])
       if av < 0 or rel < 0: continue

       if c.has_key(country):
           dav[country]=max(dav[country],av)
           drel[country]=max(drel[country],rel)
           c[country]=c[country]+1
       else:
           c.update({country:1})
           dav.update({country:av})
           drel.update({country:rel})

   for country in c.keys():
       avd.update({country:dav[country]})
       reld.update({country:drel[country]})
       date=str(year)+'-'+str(month)+'-'+'1'
       print "insert into top_bdii (month,year,country,availability,reliability,date) values ("+month+","+year+",'"+country+"',"+str(avd[country])+","+str(reld[country])+",'"+date+"');"

if __name__=='__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3])
