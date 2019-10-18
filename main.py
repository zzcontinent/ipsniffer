#-*- coding:UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header 
from email.utils import formataddr 

import array
import struct
import socket
import fcntl
import os
import sys 

import time

addr_from='zzcontinent@163.com'
addr_to='zzcontinent@163.com'
user_name='zzcontinent@163.com'
user_passwd='zzz520020'

def get_ip_address():
    #先获取所有网络接口
    #再获取每个接口的IP地址
    val = os.popen('%s/localip.sh'%(sys.path[0])).read()
    iplist = val.split()
    for i in range(10):
        #print i
        #val = os.popen('curl ifconfig.me').read()
        val = os.popen('%s/pubip.sh'%(sys.path[0])).read()
        #print val
        if val != '' :
            iplist.append('pub ip:'+val)
            break;
    return iplist

def get_host_info():
    val = os.popen(' echo `whoami` : [`lsb_release -a 2>/dev/null`] ').read()
    return val

def ip_send_mail(iptxt):
    try:
        #设置收件邮箱
        toaddrs  = addr_to 
        #设置发送邮箱
        fromaddr = addr_from 
        #设置发送邮箱的账号密码
        username = user_name 
        password = user_passwd 
                                        
        #设置SMTP服务器、端口，根据你的邮箱设置，
        server = smtplib.SMTP('smtp.163.com',25)
        #设置邮件正文，get_ip_address()返回的是list，要转换成str
        ip = '\r\n'.join(iptxt)
                                                            
        #设置邮件标题和正文
        msg = MIMEText(ip,'plain', 'utf-8')
        msg['Subject'] = get_host_info()
        msg['From'] = fromaddr
        msg['To'] = toaddrs
                                                                       
        #启动SMTP发送邮件
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()
    except Exception as e:
        print e

def is_ip_diff(ip1,ip2):
    if len(ip1) != len(ip2):
        return True 
    same_cnt=0
    for v2 in ip2:
        for v1 in ip1:
            if v1 == v2:
                same_cnt += 1
    if same_cnt == len(ip2):
        return False
    else:
        return True


if __name__ == '__main__':
    send_ip=[]
    while True:
        iptxt = get_ip_address()
        if is_ip_diff(iptxt,send_ip):
            #print "ip diff ",iptxt,send_ip
            ip_send_mail(iptxt)

        send_ip=[]
        for i in iptxt:
            send_ip.append(i)
        break 
        time.sleep(60*5)


