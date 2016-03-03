import pytest
import re
from SccpLogger.SccpLogger import EOF, TIMEOUT
from tests import sccpexecute

@pytest.mark.usefixtures("sccplogger") 

def test_call98011_1(sccplogger, params=['10.15.15.205']):
    connected = False
    expected_events = {
        re.compile(b'callState - CALL STATE IS  =(?P<State>.*)\\n'):'CallState',
    }
    #sccpexecute(request.param, 'Dial:98011')
    sccpexecute("10.15.15.205", 'Dial:98011')
    try:
        for event,content in sccplogger.waitforevents(expected_events, 5):
            print("'%s':{%s}" %(event, ','.join("'%s':'%s'" %(key, value) for key,value in content.items())))
            if event == 'CallState' and content == {'State': 'CONNECTED'}:
                connected = True
                break;
        assert connected != False
    except Exception as e:
        raise(e)
    finally:
        sccpexecute("10.15.15.205", 'Key:Soft2')	#hangup

def test_call98011_2(sccplogger, params=['10.15.15.205']):
    connected = False
    #sccpexecute(request.param, 'Dial:98011')
    sccpexecute("10.15.15.205", 'Dial:98011')
    try:
        assert sccplogger.waitforevent(b'callState - CALL STATE IS  =CONNECTED\\n', 5) == ('matched', {})
    except Exception as e:
        raise(e)
    finally:
        sccpexecute("10.15.15.205", 'Key:Soft2')	#hangup
    
