#!/usr/bin/env python3
import requests

URL_EXECUTE = 'http://%(host)s/CGI/Execute'

PHONE_EXECUTE_HEADER = '''<CiscoIPPhoneExecute>'''
EXECUTE_ITEM = '''<ExecuteItem Priority="0" URL="%(url)s"/>'''
PHONE_EXECUTE_FOOTER = '''</CiscoIPPhoneExecute>'''

def create_execute_url(url):
    push_xml = PHONE_EXECUTE_HEADER + EXECUTE_ITEM % {'url': url} + PHONE_EXECUTE_FOOTER
    return push_xml

def execute(host, data, user, password, headers={}):
    url = URL_EXECUTE % {'host' : host}
    xml = create_execute_url(data)
    data = 'XML=%s' %xml
    r = requests.post(url, data, auth=(user, password), headers=headers)
    print(r.content.decode('utf-8'))
                        
if __name__ == '__main__':
    import sys
    host = sys.argv[1]
    data = sys.argv[2]
    execute(host, data, 'cisco', 'cisco')