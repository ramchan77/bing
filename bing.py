# -*- coding: cp1252 -*-
from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import time
import glob
import string
import sys

#csv_files=glob.glob('*.csv')
input_file=sys.argv[1]
input_data=pd.read_csv(str(input_file)+'.csv',encoding='utf-8',error_bad_lines=False,sep=';')
count=0
##fd = open(str(input_file)+'_output.csv','a')
##fd.write('Given_Company;Full_Name;Title_1;Company_name;Title_2;Connections;Industry;Location;Profile_link\n')
##fd.close()
Industry=''
Title=''
Connections=''
Location=''
given_company='JURONG ENGINEERING LIMITED'
company='JURONG ENGINEERING LIMITED'
list_remove=['services','international',' (s)',' (sea)',' (singapore)',' (pte)','(s)','(sea)','(singapore)','singapore','(pte)',' pte',' ltd','pte','ltd',' private',' limited','private','limited',',','.']
head_remove=[' - LinkedIn',' | LinkedIn',' | …',' - …',' …',' ...']
for index,given_company_name in input_data.itertuples():
    match_count=1
    count+=1
    print(str(count)+' '+str(given_company_name))
    given_company=given_company_name
    company=given_company_name
    for li in list_remove:
        given_company=given_company.lower().replace(li,'')
        company=company.lower().replace(li,'')
    given_company=given_company.lower().replace(' ','%20')
    url='https://www.bing.com/search?q=+site%3Alinkedin.com%2Fin+%22'+given_company+'%22+%22location+singapore%22'
    while match_count>0:
        Industry=''
        Title=''
        Connections=''
        Location=''
        content=requests.get(url)
        soup = BeautifulSoup(content.content)
        result=soup.find("ol",{"id":"b_results"})
        try:
            items=result.find_all('li',{'class':'b_algo'})
        except:
            break
        match_count=str(items).lower().count(company)
        print(company)
        print(match_count)
        if match_count==0:
            break
        for ii in items:
            header_text=ii.find('h2').text.encode("utf-8")
            for hr in head_remove:
                header_text=header_text.replace(hr,'')
            headers=header_text.split(' - ')
            fullname=headers[0]
            try:
                title_1=headers[1]
            except:
                title_1=''
            try:
                link_company=headers[2]
            except:
                link_company=''
            #print('Given Company: '+given_company_name)
            profile_link=ii.find('h2').a.get('href')
            try:
                for li in ii.find('div',{'class':'b_vlist2col'}).find_all('li'):
                    li=li.text.encode("utf-8")
                    if li.startswith('Title'):
                        Title=li
                        Title=Title.replace('Title: ','')
                        Title=Title.replace(' …','')
                    if li.startswith('500+') or li.startswith('Connections'):
                        Connections=li
                        Connections=Connections.replace(' connections','')
                        Connections=Connections.replace('Connections: ','')
                    if li.startswith('Industry'):
                        Industry=li
                        Industry=Industry.replace('Industry: ','')
                        Industry=Industry.replace(' …','')
                    if li.startswith('Location'):
                        Location=li
                        Location=Location.replace('Location: ','')
                try:   
                    fd = open(str(input_file)+'_output.csv','a')
                    fd.write('"'+str(given_company_name.encode("utf-8"))+'";"'+str(fullname)+'";"'+str(title_1)+'";"'+str(link_company)+'";"'+str(Title)+'";"'+str(Connections)+'";"'+str(Industry)+'";"'+str(Location)+'";"'+str(profile_link.encode("utf-8"))+'"\n')
                    fd.close()
                except Exception as e:
                    print(str(e))
            except Exception as e:
                print(e)
            #print('Industry: '+Industry)
            #print('Connections: '+Connections)
            #print('Title: '+Title)
            #print('Location: '+Location)
            #print('-----------------------------------')
        try:
            url='https://www.bing.com'+str(soup.find('a',{'title':'Next page'}).get('href'))
        except:
            break
        #match_count=str(items).lower().count(company)
        #print(company)
        #print(match_count)
    
