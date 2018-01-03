from transitions.extensions import GraphMachine
import random
import time
import sys
import requests
from bs4 import BeautifulSoup
import os
import re
import urllib.parse
import urllib.request
from urllib.request import urlopen
import json
import zipfile
import imghdr
import shutil

def get_web_page(url):
    resp = requests.get(
        url=url
    )
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text

def parse(dom):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=dom, headers=headers)
    soup = BeautifulSoup(urlopen(req), 'html.parser')
    links = soup.find_all('img')
    img_urls = []

    for link in links:
        time.sleep(0.05)
        try:
            img_urls.append(link['data-src'])
        except:
            nothing=1
    return img_urls


def save(img_urls):
    now=str(time.strftime("%Y_%m_%d_%H_%M_%S"))
    os.makedirs(now)
    with zipfile.ZipFile(now + ".zip","w") as zf:
        count=1
        for img_url in img_urls:
            s=str(count)
            try:
                urllib.request.urlretrieve(img_url,s)
                s2=s+"."+imghdr.what(s)
                os.rename(s,s2)
                zf.write(s2)
                shutil.move(s2,now)
                count=count+1
            except Exception as e:
                print(e)
    #shutil.move("compress.zip",now)
    return now
    ####################

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )
    condition=0
    def start(self,update):
        if update.message.text.lower()=='/start':
            condition=0
            return 1
    def on_enter_introduction(self,update):
        condition=0
        update.message.reply_text("Please choose which web to search \n(1.)google\n(2.)youtube\n(3.)baidu\n(4.)google_pic (with English only)")

    def is_going_to_google(self, update):
        if update.message.text.lower()=='google' or update.message.text.lower()=='1':
            print(str(self.condition) + "is_going_to_google")
            if self.condition==0:
                self.condition=1
                update.message.reply_text("Please input keywords(google search)")
                print (update.message.text.lower())
                return 1

    def is_going_to_youtube(self, update):
        if update.message.text.lower()=='youtube' or update.message.text.lower()=='2':
            print(str(self.condition) + "is_going_to_youtube")
            if self.condition==0:
                self.condition=2
                update.message.reply_text("Please input keywords(youtube search)")
                print (update.message.text.lower())
                return 1


    def is_going_to_baidu(self, update):
        if update.message.text.lower()=='baidu' or update.message.text.lower()=='3':
            print(str(self.condition) + "is_going_to_baidu")
            if self.condition==0:
                self.condition=3
                update.message.reply_text("Please input keywords(baidu search)")
                print (update.message.text.lower())
                return 1
    def is_going_to_google_pic(self,update):
        if update.message.text.lower()=='google_pic' or update.message.text.lower()=='4':
            print(str(self.condition) + "is_going_to_google_pic")
            if self.condition==0:
                self.condition=4
                update.message.reply_text("Please input keywords(google_pic search)")
                print (update.message.text.lower())
                return 1


    def is_going_to_print_text(self, update):
        print (update.message.text.lower())
        return len(update.message.text)>=1

    def on_enter_print_text(self, update):
        #update.message.reply_text(str(random.randint(0,100)))
        print(str(self.condition) + "on_enter_print_text")
        if self.condition==1:
            s1="http://www.google.com.tw/search?q="+str(update.message.text).replace(' ','+')
            update.message.reply_text(s1)
        elif self.condition==2:
            s1="https://www.youtube.com/results?search_query="+str(update.message.text).replace(' ','+')
            update.message.reply_text(s1)
        elif self.condition==3:
            s1="http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd="+str(update.message.text).replace(' ','_')+"&rsv_pq=81ca67440000fe45&rsv_t=d348ta%2Fm4HoXNKeiM%2FIx%2FvfWggzntyPkayF1xhf0hhkW9wJexDlwx2jH%2Bls&rqlang=cn&rsv_enter=1&rsv_sug3=11&rsv_sug1=1&rsv_sug7=100&rsv_sug2=0&inputT=1694&rsv_sug4=1695"
            update.message.reply_text(s1)
        elif self.condition==4:
            s1="https://www.google.com.tw/search?q="+str(update.message.text).replace(' ','+')+"&tbm=isch"
            update.message.reply_text(s1)
            print (s1)
            try:
                update.message.reply_text("Testing URL")
                current_page = get_web_page(s1)
                update.message.reply_text("Get URL")
                if current_page:
                    update.message.reply_text("Testing parse")
                    img_urls=parse(s1)
                    update.message.reply_text("Saving")
                    s=save(img_urls)
                    print(s+".zip")
                    update.message.reply_text("Opening Zip")
                    fileopen=open(s+".zip","rb")
                    update.message.reply_text("Sending Zip")
                    update.message.reply_document(fileopen)
                    update.message.reply_text("Send Zip complete")
                    print ("End")
            except:
                update.message.reply_text("Some error occur when processing pic")
                print ("Not normal end")
        else:
            update.message.reply_text("Fail")
        self.condition=0
        self.go_back(update)
        #######



