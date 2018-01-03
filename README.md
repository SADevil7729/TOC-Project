# TOC Project 2017~2018
# Edit this document in 2018/1/3



# Author
NCKU CSIE108
F74041179



# Introduction
A telegram bot based on a finite state machine
With Function 1 2 3 4
(1.)google search
(2.)youtube search
(3.)baidu search
(4.)google_pic search



# Fuction
In (1,2,3,4) you can type a keyword and you can get a link to different search engine

In (4)google_pic search has add a function that can download picture and compress it into .zip file
and send it to user (With English only)

if you type in other language you will only get a link to google picture search 
and you will not get a zip file



### Prerequisite
* Python 3




### Secret Data

`API_TOKEN` and `WEBHOOK_URL` in app.py **MUST** be set to proper values.
Otherwise, you might not be able to run your code.




### Run Locally
You can either setup https server or using `ngrok` as a proxy.

**`ngrok` would be used in the following instruction**

```sh
ngrok http 5000
```

After that, `ngrok` would generate a https URL.

You should set `WEBHOOK_URL` (in app.py) to `your-https-URL/hook`.




#### Run the sever

```sh
python3 app.py
```




## Finite State Machine
![fsm](./img/show-fsm.png)
