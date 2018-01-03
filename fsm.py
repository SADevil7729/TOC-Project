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
        url=url,
        cookies={'over18': '1'}
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
        update.message.reply_text("Please choose which web to search \n(1.)google\n(2.)youtube\n(3.)baidu\n(4.)google_pic")

    def is_going_to_google(self, update):
        if update.message.text.lower()=='google':
            print(str(self.condition) + "is_going_to_google")
            if self.condition==0:
                self.condition=1
                update.message.reply_text("Please input keywords(google search)")
                print (update.message.text.lower())
                return 1

    def is_going_to_youtube(self, update):
        if update.message.text.lower()=='youtube':
            print(str(self.condition) + "is_going_to_youtube")
            if self.condition==0:
                self.condition=2
                update.message.reply_text("Please input keywords(youtube search)")
                print (update.message.text.lower())
                return 1


    def is_going_to_baidu(self, update):
        if update.message.text.lower()=='baidu':
            print(str(self.condition) + "is_going_to_baidu")
            if self.condition==0:
                self.condition=3
                update.message.reply_text("Please input keywords(baidu search)")
                print (update.message.text.lower())
                return 1
    def is_going_to_google_pic(self,update):
        if update.message.text.lower()=='google_pic':
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
        elif self.condition==2:
            s1="https://www.youtube.com/results?search_query="+str(update.message.text).replace(' ','+')
        elif self.condition==3:
            s1="http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd="+str(update.message.text).replace(' ','_')+"&rsv_pq=81ca67440000fe45&rsv_t=d348ta%2Fm4HoXNKeiM%2FIx%2FvfWggzntyPkayF1xhf0hhkW9wJexDlwx2jH%2Bls&rqlang=cn&rsv_enter=1&rsv_sug3=11&rsv_sug1=1&rsv_sug7=100&rsv_sug2=0&inputT=1694&rsv_sug4=1695"
        elif self.condition==4:
            s1="https://www.google.com.tw/search?q="+str(update.message.text).replace(' ','+')+"&tbm=isch"
            print (s1)
            update.message.reply_text("Testing URL")
            try:
                current_page = get_web_page(s1)

                update.message.reply_text("Get URL")
                if current_page:
                    update.message.reply_text("Testing parse")
                    img_urls=parse(s1)
                    update.message.reply_text("Saving")
                    s=save(img_urls)
                    #time.sleep(0.1)
                    print(s+".zip")
                    update.message.send_document(open(s+".zip","rb"))
                print ("End")
            except:
                print ("Not normal end")

        else:
            update.message.reply_text("Fail")
            self.condition=0
            self.go_back(update)
        self.condition=0
        update.message.reply_text(s1)
        self.go_back(update)
        #######



