import pytest
import re
from SccpLogger.SccpLogger import SccpLogger, EOF, TIMEOUT

def handle_tone(ssh, index, child_result_list):
   tone = int(ssh.match.group(2))
   dir = int(ssh.match.group(3))
   return 'Tone', {'State':ssh.match.group(1).decode('utf-8'),'Type':sccp.lookup_tone(tone),'Direction':sccp.lookup_tonedirection(dir)}

@pytest.yield_fixture(scope="session", autouse=True, params=["10.15.15.205"])
def sccplogger(request):
    options={'username':'cisco','password':'cisco','shelluser':'default','shellpasswd':'user','logfilename':'output.log'}
    #hostname = '10.15.15.205'
    hostname = request.param
    _logger = SccpLogger(hostname, options)
    try:
        print("\nconnecting to %s..." %hostname)
        _logger.connect()
        print("connected")
        _logger.login()
        print('logged in to shell. setting up debug environment...')
        _logger.setup_debug()
        print('starting strace...')
        _logger.start_strace()
        print('ready to process events...\n')
        yield _logger
        #_logger.disconnect()
    except TIMEOUT:
        print("Connection timed out")
    except EOF:
        print("Disconnect from phone")
    except KeyboardInterrupt:
        print("Interrupted by User")
    except Exception as e:
        print("Exception occured: %s" %e)
