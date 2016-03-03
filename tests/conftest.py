import pytest
import re
from SccpLogger.SccpLogger import SccpLogger, EOF, TIMEOUT

def handle_tone(ssh, index, child_result_list):
   tone = int(ssh.match.group(2))
   dir = int(ssh.match.group(3))
   return 'Tone', {'State':ssh.match.group(1).decode('utf-8'),'Type':sccp.lookup_tone(tone),'Direction':sccp.lookup_tonedirection(dir)}

@pytest.yield_fixture(scope="session", autouse=True)
def sccplogger(request):
    events = {
        re.compile(b'processSoftkey (?P<SoftkeyIndex>\d) DOWN IN\\n'):'SoftKeyDown',
        re.compile(b'processSoftkey (?P<SoftkeyIndex>\d) DOWN OUT\\n'):'SottKeyUp',
        re.compile(b'Received SOFT: (?P<SoftkeyIndex>\d)\\n'):'SoftKeyPressed',
        re.compile(b'setAudioPath \((?P<Path>.*)\)\\n'):'AudioPath',		# HANDSET / SPEAKER / NONE
        re.compile(b'DisplayTask:\? - Active Call Count: (?P<Num>\d)\\n'):'ActiveCallCount',
        re.compile(b'DisplayTask:\? - ([a-zA-Z]+)=(true|false) ([a-zA-Z]+)=(true|false)\\n'):'DisplayState',
        re.compile(b'DisplayTask:\? - ([a-zA-Z]+)=(true|false)\\n'):'DisplayState',
        re.compile(b'InputManager:\? - Received DTMF: (?P<Num>\d+)\\n'):'ReceivedDTMF',
        re.compile(b'Notifying model of controller with name Line-(?P<LineNum>\d+)  event \d+\\n'):'LineUsed',
        re.compile(b'setOverviewCallAndLineState - DN=(?P<DN>\d+) lineState=(?P<LineState>.*) old lineWeight=.* new lineWeight=.*\\n'):'CallAndLineState',
        re.compile(b'setText \( "(?P<Text>.*)" \)\\n'):'StatusPrompt',		# Ring out / Call Proceed / Connected / Your current options
        re.compile(b'Tone-AUDIBLE FEEDBACK: (?P<State>.*):\(ToneType: (?P<Type>\d+), ToneDir: (?P<Direction>\d+)\)\\n'):handle_tone,
        re.compile(b'callState - CALL STATE IS  =(?P<State>.*)\\n'):'CallState',
        re.compile(b'Call View: Call-(?P<CallNum>\d+) draw\\n'):'CallView',
        re.compile(b'processSoftkey (?P<SoftKey>\d) (?P<UpDown>UP|DOWN) (?P<InOut>IN|OUT)\\n'):'SoftKey',
        re.compile(b'MediaTermination_open(?P<Gress>.*)\\n'):'MediaTermination',
        re.compile(b'STREAM- (?P<Gress>.*)\\n'):'Stream',
        re.compile(b'(?P<ORC>In ORC Bit Rate.*)\\n'):'OpenReceiveChannel',
        re.compile(b'(?P<SMT>In SMT Bit Rate.*)\\n'):'StartMediaTransmission',
        re.compile(b'openEgressChannel, multicastListenIp=(?P<MultiCastIP>.*), localPort=(?P<Port>\d+), mediaPayloadType=(?P<Type>\d)\\n'):'OpenEgressChannel',
        re.compile(b'openIngressChannel, remoteIpAddr=(?P<IP>.*), remotePort=(?P<Port>\d+), mediaPayloadType=(?P<Type>\d)\\n'):'OpenIngressChannel',
    }
    options={'username':'cisco','password':'cisco','shelluser':'default','shellpasswd':'user','logfilename':'output.log'}
    hostname = '10.15.15.205'
    _logger = SccpLogger(hostname, options)
    try:
        print("connecting to %s..." %hostname)
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
