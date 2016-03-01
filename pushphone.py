import requests

def httppush(ip, uri, username, password):
  try:
    xml = "<CiscoIPPhoneExecute><ExecuteItem Priority=\"0\" URL=\"%s\"/></CiscoIPPhoneExecute>" %(uri)
    url = 'http://%s/CGI/Execute' %(ip)
    payload = {'XML': xml}
    headers={"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain", "Connection": "close", "Content-Length": "%d" %len(xml)}
    auth = (username, password)
    r = requests.post(url, data=payload, auth=auth, headers=headers)
    print(r.status_code)
    print(r.headers)
    print(r.text)
  except Exception as e:
    print e

httppush('10.15.15.205', 'Dial:666', 'cisco', 'cisco')
