#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016-12-02

@author: gavin
'''
import sys
import hmac
import base64
import hashlib
import urllib
import time
import uuid
import requests

ALIYUN_ACCESS_DOMAIN = "AccessDomain"
ALIYUN_ACCESS_KEY_ID = "AccessKeyId"
ALIYUN_ACCESS_KEY_SECRET = "AccessKeySecret"
ALIYUN_ACCOUNT_NAME = "AccountName"


class AliyunEmailMonitor:
    def __init__(self):
        self.access_id = ALIYUN_ACCESS_KEY_ID
        self.access_secret = ALIYUN_ACCESS_KEY_SECRET
        self.account_name = ALIYUN_ACCOUNT_NAME
        self.domain = ALIYUN_ACCESS_DOMAIN

    def sign(self, parameters, accessKeySecret):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
        canonicalizedQueryString = ''

        for (k, v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        stringToSign = 'GET&%2F&' + self.percent_encode(canonicalizedQueryString[1:])   # 使用get请求方法

        h = hmac.new(accessKeySecret + "&", stringToSign, hashlib.sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def percent_encode(self, encodeStr):
        encodeStr = str(encodeStr)
        res = urllib.quote(encodeStr.decode(sys.stdin.encoding).encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def make_url(self, params):
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = {
            'Format': 'JSON',
            'Version': '2015-11-23',
            'AccessKeyId': self.access_id,
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureVersion': '1.0',
            'SignatureNonce': str(uuid.uuid1()),
            'Timestamp': timestamp,
        }
        for key in params.keys():
            parameters[key] = params[key]

        signature = self.sign(parameters, self.access_secret)
        parameters['Signature'] = signature

        url = "http://" + self.domain + "/?" + urllib.urlencode(parameters)
        return url

    def send_email(self, to_address, subject, text, from_alias=None):
        payload = {
            'Action': 'SingleSendMail',
            'AccountName': self.account_name,
            'ReplyToAddress': True,
            'AddressType': 0,
            'ToAddress': to_address,
            # 'FromAlias': from_alias,
            'Subject': subject,
            'HtmlBody': text,
        }
        if from_alias is not None:
            payload['FromAlias'] = from_alias

        url = self.make_url(payload)
        request = requests.get(url)
        print request.text

if __name__ == '__main__':
    email_monitor = AliyunEmailMonitor()
    email_monitor.send_email('test@test.com', '标题', '内容')
