# -*- coding: cp1252 -*-
from bs4 import BeautifulSoup
import urllib2
import requests
import pandas as pd
import time
import glob
import string
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re

count=0
##fd = open('bank_output.csv','a')
##fd.write('Given_link;Full_Name;Title_1;Company_name;Title_2;Connections;Industry;Location;Profile_link\n')
##fd.close()
Industry=''
Title=''
Connections=''
Location=''
head_remove=[' - LinkedIn',' | LinkedIn',' | …',' - …',' …',' ...']
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
browser = webdriver.Chrome(executable_path='C:\Users\lenovo\Desktop\python\chromedriver.exe',chrome_options=options,desired_capabilities=capa)
time.sleep(1)
browser.get("https:\\www.bing.com")
try:
    wait = WebDriverWait(browser, 12)
    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sb_form_q"]')))
except:
    time.sleep(12)
time.sleep(2)
def get_data(result):
    Industry=''
    Title=''
    Connections=''
    Location=''
    items=[]    
    try:
        items=result.find_all('li',{'class':'b_algo'})
    except:
        print(items)
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
                fd = open('bank_output.csv','a')
                fd.write('"'+str(fullname)+'";"'+str(title_1)+'";"'+str(link_company)+'";"'+str(Title)+'";"'+str(Connections)+'";"'+str(Industry)+'";"'+str(Location)+'";"'+str(profile_link.encode("utf-8"))+'"\n')
                fd.close()
                print('inserted')
            except Exception as e:
                print(str(e))
        except Exception as e:
            print(e)
    url='https://www.bing.com'+str(result.find('a',{'title':'Next page'}).get('href'))
    return url
search_list=['site:hk.linkedin.com   "HR" "Hospital & Health Care" "location Hongkong"  -dir']
for link in search_list:
    next_page=True
    try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sb_form_q"]')))
            editor=browser.find_element_by_xpath('//*[@id="sb_form_q"]')
            editor.clear()
            editor.send_keys(link)
            browser.find_element_by_xpath('//*[@id="sb_form_go"]').click()
    except Exception as e:
        browser.get("https:\\www.bing.com")
        continue
    s_count=0
    count+=1
    print(str(count)+' '+str(link))
    url='https://www.bing.com/search?q='+str(link)
    try:
        #content=requests.get(url)
        #soup = BeautifulSoup(content.content)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="b_results"]')))
        result=BeautifulSoup(browser.find_element_by_xpath('//*[@id="b_results"]').get_attribute("outerHTML"))
        next_page_url=get_data(result)
        print(next_page_url)
    except Exception as e:
        print(e)
    while next_page:
        try:
            browser.get(next_page_url)
            wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="b_results"]')))
            result=BeautifulSoup(browser.find_element_by_xpath('//*[@id="b_results"]').get_attribute("outerHTML"))
            next_page_url=get_data(result)
            print(next_page_url)
        except Exception as e:
            print(e)



