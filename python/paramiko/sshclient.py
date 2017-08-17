#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import stat
import socket
import paramiko
import traceback
import logging
import time

# paramiko日志
# paramiko.util.log_to_file('/tmp/sshclient.log')

class SSHClient(object):
    def __init__(self, hostname, port=22, username=None, password=None, key_filename=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.client = None
        self.sftp = None

    def client_conn(self, timeout=None):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if self.username and self.password:
            try: client.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password, timeout=timeout)
            except: client = None
        elif self.username and self.key_filename:
            try: client.connect(hostname=self.hostname, port=self.port, username=self.username, key_filename=self.key_filename, timeout=timeout)
            except: client = None
        else: client = None
        self.client = client
        if self.client is not None:
            self.sftp = self.client.open_sftp()

    def client_close(self):
        if self.sftp is not None:
            self.sftp.close()
            self.sftp = None
        if self.client is not None:
            self.client.close()
            self.client = None

    @property
    def is_conn(self):
        return self.client is not None

    @property
    def is_root(self):
        return self.username is 'root'

    def exec_command(self, command, timeout=None):
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            std_out = stdout.read()
            std_err = stderr.read()
            return (std_out, std_err)
        except socket.timeout: return ('', 'timeout')
        except: return ('', traceback.format_exc())

    def send_command(self, command):
        shell = self.client.invoke_shell()
        time.sleep(0.1)
        if not self.is_root:
            shell.send('sudo su\n')
        buff = ''
        while not buff.endswith('# '):
            resp = shell.recv(1024)
            buff += resp
        shell.send(command + '\n')
        buff = ''
        while not buff.endswith('# '):
            resp = shell.recv(1024)
            buff += resp
        shell.close()
        return (buff, '')

    def file_get(self, remote_fpath, local_fpath):
        self.sftp.get(remote_fpath, local_fpath)

    def file_put(self, local_fpath, remote_fpath):
        self.sftp.put(local_fpath, remote_fpath)

    def file_read(self, fpath):
        with self.sftp.open(fpath, mode='r') as fopen:
            return fopen.read()

    def file_write(self, fpath, content):
        with self.sftp.open(fpath, mode='w') as fopen:
            fopen.write(content)

    def remove(self, fpath):
        self.sftp.remove(fpath)

    def rename(self, oldpath, newpath):
        self.sftp.rename(oldpath, newpath)

    def mkdir(self, path):
        self.sftp.mkdir(path)

    def rmdir(self, path):
        self.sftp.rmdir(path)

    def isdir(self, path):
        try:
            st = self.sftp.stat(path)
        except:
            return False
        return stat.S_ISDIR(st.st_mode)

    def isfile(self, path):
        try:
            st = self.sftp.stat(path)
        except:
            return False
        return stat.S_ISREG(st.st_mode)

class MYSSHClient(SSHClient):
    pass

if __name__ == '__main__':
    pass
