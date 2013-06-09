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

def previous_my(m,y):

    if m==1:
        return 12,y-1
    else:
        return m-1,y


if __name__=='__main__':

   month=int(sys.argv[1])
   year=int(sys.argv[2])

   month1,year1=previous_my(month,year)
   month2,year2=previous_my(month1,year1)

   date1=str(year2)+'-'+str(month2)+'-'+str(1)
   date2=str(year)+'-'+str(month)+'-'+str(1)

   date1='2012-6-1'
   date1='2013-5-1'

   list=psql("select site,date from aru where date >= '"+date1+"' and date <= '"+date2+"' and (availability < 70 or reliability<75)")
   d={}
   for l in list:
       if d.has_key(l[0]): d[l[0]]=d[l[0]]+1
       else:
           d.update({l[0]:1})
#   count=0
#   for k in d.keys():
#       if d[k]==3: 
#           count=count+1
#           print k


#   print count
   print d


   

