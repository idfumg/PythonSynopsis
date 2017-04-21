#!/usr/bin/env python

import smtplib
import socket
import sys
import getpass
import imaplib
import email

from collections import Mapping


"""
Send and receive emails module.
"""


def merge_settings(request_setting, session_setting):
    if session_setting is None:
        return request_setting

    if request_setting is None:
        return session_setting

    if not (isinstance(session_setting, Mapping) and
            isinstance(request_setting, Mapping)):
        return request_setting

    merged = dict(session_setting)
    merged.update(request_setting)
    merged = dict((k, v) for (k, v) in merged.items() if v is not None)
    
    return merged


class SMTPAdapter:
    def __init__(self):
        self.conn = None
        self.auth = None
        self.logined = False
        self.tls = None


    def connect(self, url, port, auth, tls = True):
        if not port:
            port = self.make_default_port()

        self.auth = auth
        self.tls = tls

        if not self.conn:
            try:
                self.conn = smtplib.SMTP('smtp.%s' % url, port)
                self.conn.ehlo()
                if tls:
                    self.conn.starttls()
                self.conn.ehlo()
            except (socket.gaierror, socket.error, socket.herror,
                    smtplib.SMTPException) as e:
                print('[-] Connection failed')
                print('Reason: %s' % e)

        if not self.logined:
            try:
                self.conn.login(auth[0], auth[1])
                self.logined = True
            except smtplib.SMTPException as e:
                print('[-] Login failed')
                print('Reason: %s' % e)
                self.conn.close()

        return self


    def send(self, data):
        if len(data) == 3:
            data = (data[0], self.auth[0], data[1], data[2])
        msg = self.collect_msg(data)
        try:
            self.conn.sendmail(data[1], data[0], msg)
        except smtplib.SMTPException as e:
            print('[-] Send failed')
            print('Reason: %s' % e)
            self.conn.close()

        return self


    def collect_msg(self, data):
        return '\n'.join(['To: %s' % data[0],
                          'From: %s' % data[1],
                          'Subject: %s' % data[2],
                          '\n%s\n\n' % data[3]])


    def make_default_port(self):
        if self.tls:
            return 587
        return 25


    def quit(self):
        self.conn.quit()


    def __enter__(self):
        return self


    def __exit__(self, *ignore):
        self.quit()


class IMAPAdapter:
    class Message(dict):
        def __init__(self, msg = {}):
            super().__init__(msg)


        def __str__(self):
            return '\n'.join(['From: %s' % self['from'],
                              'To: %s' % self['to'],
                              'Subject: %s' % self['subject'],
                              'Date: %s' % self['date'],
                              'Body: %s' % self['body']])


    def __init__(self):
        self.conn = None
        self.auth = None
        self.tls = None
        self.logined = False
        self.uids = None


    def connect(self, url, port, auth, tls = True):
        if not port:
            port = self.make_default_port()

        self.tls = tls
        self.auth = auth

        if not self.conn:
            try:
                if self.tls:
                    self.conn = imaplib.IMAP4_SSL('imap.%s' % url)
                else:
                    self.conn = imaplib.IMAP4('imap.%s' % url)
            except Exception as e:
                print('[-] Connection failed')
                print('Reason: %s' % e)

        if not self.logined:
            try:
                self.conn.login(self.auth[0], self.auth[1])
                self.conn.list()
                self.logined = True
            except Exception as e:
                print('[-] Login failed')
                print('Reason: %s' % e)
                self.conn.close()

        return self


    def get_raw(self, uid):
        try:
            result, data = self.conn.uid('fetch', uid, '(RFC822)')
            raw_email = data[0][1]
        except Exception as e:
            print('[-] Fetch failed')
            print('Reason: %s' % e)
            self.conn.close()

        return raw_email


    def get(self, num = None, data = None, encoding = 'utf-8'):
        if num is not None:
            msg = self.prepare_msg(self.get_raw(self.uids[num - 1]), encoding)
            yield msg
            return

        for uid in self.uids:
            msg = self.prepare_msg(self.get_raw(uid), encoding)

            if data:
                for key in data.keys():
                    if data[key] != msg[key]:
                        msg = None
                        break

            if msg is not None:
                yield msg


    def prepare_msg(self, msg, encoding = 'utf-8'):
        msg = email.message_from_string(msg.decode(encoding))

        m = self.Message()
        m['to'] = msg['to']
        m['from'] = email.utils.parseaddr(msg['from'])[1]
        m['subject'] = msg['subject']
        m['body'] = msg.get_payload()
        m['date'] = email.utils.parsedate_to_datetime(msg['date'])

        return m


    def inbox(self):
        self.conn.select('inbox')
        self.search()

        return self


    def delete(self, num):
        self.conn.uid('STORE', self.uids[num - 1], '+X-GM-LABELS', '\\Trash')
        self.conn.expunge()

        return self


    def select(self, query):
        self.conn.select(query)
        self.seach()

        return self


    def search(self):
        try:
            result, data = self.conn.uid('search', None, 'ALL')
            self.uids = list(reversed(data[0].split()))
        except Exception as e:
            print('[-] Search failed')
            print('Reason: %s' % e)
            self.conn.close()

        return self


    def size(self):
        return len(self.uids)

    
    def make_default_port(self):
        if self.tls:
            return 143
        return 993


    def quit(self):
#        self.conn.close()
        self.conn.logout()


    def __enter__(self):
        return self


    def __exit__(self, *ignore):
        self.quit()


class Session:
    def __init__(self):
        self.auth = None
        self.port = None
        self.tls = True
        self.url = None
        self.adapters = dict()

        self.mount('smtp', SMTPAdapter())
        self.mount('imap', IMAPAdapter())
        
    
    def connect(self, method, url = None,
                port = None,
                tls = None,
                auth = None):
        if auth is not None:
            self.auth = merge_settings(auth, self.auth)
        self.tls = merge_settings(tls, self.tls)
        self.port = merge_settings(port, self.port)
        self.url = merge_settings(url, self.url)

        adapter = self.get_adapter(method = method)

        return adapter.connect(self.url, self.port, self.auth, self.tls)


    def mount(self, prefix, adapter):
        self.adapters[prefix] = adapter


    def get_adapter(self, method):
        for (prefix, adapter) in self.adapters.items():
            if method.lower().startswith(prefix):
                return adapter

        raise Exception("No connection adapters were found for '%s'" % method)
        

def session():
    return Session()


def connect(method, url, **kwargs):
    """
    Constructs and send request to the server related on method param.

    :param method: method for request. (smtp, imap)
    :param url: server url.
    :param from: a field 'from' in request.
    :param data: a fields 'To', 'Subject', 'Body' in request.
    :param tls: enable secure socket.
    """
    
    s = session()
    return s.connect(method = method, url = url, **kwargs)


def smtp(url, **kwargs):
    """
    Sends smtp request.

    :param url: a server address.
    :param data: a tuple of data to send to a server (to, sub, body).
    """
    
    return connect('smtp', url, **kwargs)


def imap(url, **kwargs):
    """
    Sends imap request.

    :param url: a server address.
    """

    return connect('imap', url, **kwargs)


#######################
# Usage
#######################

def get_auth():
    user = str(input("User: ")).lower().strip()
    passwd = str(getpass.getpass("Passwd: ")).lower().strip()

    return user, passwd

# with smtp("gmail.com", auth = get_auth()) as smtp:
#     for i in range(1, 4):
#         smtp.send(('idfumg@gmail.com', 'Test subject', 'Test body'))

# with imap("gmail.com", auth = get_auth()) as imap:
#     imap.inbox()
#     for msg in imap.get(data = {}):
#         print(msg)

s = session()
s.auth = get_auth()
s.url = 'gmail.com'

with s.connect('smtp') as smtp:
    pass

with s.connect('imap') as imap:
    imap.inbox()
