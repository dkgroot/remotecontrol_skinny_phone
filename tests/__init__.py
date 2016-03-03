import pytest
import re
from SccpLogger.SccpLogger import SccpLogger, EOF, TIMEOUT

def sccpexecute(host, data, user='cisco', password='cisco', headers={}):
    import requests

    URL_EXECUTE = 'http://%(host)s/CGI/Execute'
    PHONE_EXECUTE_HEADER = '''<CiscoIPPhoneExecute>'''
    EXECUTE_ITEM = '''<ExecuteItem Priority="0" URL="%(url)s"/>'''
    PHONE_EXECUTE_FOOTER = '''</CiscoIPPhoneExecute>'''

    url = URL_EXECUTE % {'host' : host}
    xml = PHONE_EXECUTE_HEADER + EXECUTE_ITEM % {'url': data} + PHONE_EXECUTE_FOOTER
    data = 'XML=%s' %xml
    r = requests.post(url, data, auth=(user, password), headers=headers)
    if r.status_code != 200:
        raise Exception("sccpexecture exception: %d: '%s'" %(r.status_code, r.content.decode('utf-8')))

