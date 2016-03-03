#!/usr/bin/env python3
import re
from SccpLogger.SccpLogger import SccpLogger, EOF, TIMEOUT
from pprint import pprint
from optparse import OptionParser

def main():
    def handle_read(ssh, index, child_result_list):
       opcode = int(ssh.match.group(2), 16)
       if opcode == 256: # Skip KeepAlive
           return None
       else:
           yield 'Read', {'Read':sccp.lookup_opcode(opcode),'Length':int(ssh.match.group(1))}

    def handle_write(ssh, index, child_result_list):
       opcode = int(ssh.match.group(2), 16)
       if opcode == 0: # Skip KeepaliveAck
           return None
       else:
           return 'Write', {'Written':sccp.lookup_opcode(opcode),'Length':int(ssh.match.group(1))}
    
    def handle_tone(ssh, index, child_result_list):
       tone = int(ssh.match.group(2))
       dir = int(ssh.match.group(3))
       return 'Tone', {'State':ssh.match.group(1).decode('utf-8'),'Type':sccp.lookup_tone(tone),'Direction':sccp.lookup_tonedirection(dir)}

    events = {
        #re.compile(b'Read Sccp Length: (?P<length>\d+) messageType: (?P<type>0x[0-9a-fA-F]+) avalable:'):handle_read,
        #re.compile(b'Writing Sccp Length: (?P<length>\d+) for SCCP MSG: (?P<type>0x[0-9a-fA-F]+)\\n'):handle_write,
        
        # device control
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
        
        # call control
        re.compile(b'Tone-AUDIBLE FEEDBACK: (?P<State>.*):\(ToneType: (?P<Type>\d+), ToneDir: (?P<Direction>\d+)\)\\n'):handle_tone,
        re.compile(b'callState - CALL STATE IS  =(?P<State>.*)\\n'):'CallState',
        re.compile(b'Call View: Call-(?P<CallNum>\d+) draw\\n'):'CallView',
        re.compile(b'processSoftkey (?P<SoftKey>\d) (?P<UpDown>UP|DOWN) (?P<InOut>IN|OUT)\\n'):'SoftKey',
        
        # rtp flow
        re.compile(b'MediaTermination_open(?P<Gress>.*)\\n'):'MediaTermination',
        re.compile(b'STREAM- (?P<Gress>.*)\\n'):'Stream',
        re.compile(b'(?P<ORC>In ORC Bit Rate.*)\\n'):'OpenReceiveChannel',
        re.compile(b'(?P<SMT>In SMT Bit Rate.*)\\n'):'StartMediaTransmission',
        re.compile(b'openEgressChannel, multicastListenIp=(?P<MultiCastIP>.*), localPort=(?P<Port>\d+), mediaPayloadType=(?P<Type>\d)\\n'):'OpenEgressChannel',
        re.compile(b'openIngressChannel, remoteIpAddr=(?P<IP>.*), remotePort=(?P<Port>\d+), mediaPayloadType=(?P<Type>\d)\\n'):'OpenIngressChannel',
    }

    # Parse Command Line Options    
    parser = OptionParser(usage="%prog <hostname>", version="%prog 0.1")
    parser.add_option('-n', '--username', action='store', type='string', dest='username', default='cisco', help='ssh username to connect to phone')
    parser.add_option('-p', '--password', action='store', type='string', dest='password', default='cisco', help='ssh password to connect to phone')
    parser.add_option('-a', '--shelluser', action='store', type='string', dest='shelluser', default='default', help='shell username to login to the phone')
    parser.add_option('-b', '--shellpass', action='store', type='string', dest='shellpasswd', default='user', help='shell password to login to the phone')
    parser.add_option('-l', '--logfile', action='store', type='string', dest='logfile', help='log ssh output to logfile')
    (options, args) = parser.parse_args()    
    if len(args) != 1:
            parser.error('incorrect number of arguments')
    hostname = args[0]
    
    # Call SccpLogger Library
    sccp = SccpLogger(hostname, vars(options))
    try:
        print("connecting to %s..." %hostname)
        sccp.connect()
        print("connected")
        sccp.login()
        print('logged in to shell. setting up debug environment...')
        sccp.setup_debug()
        print('starting strace...')
        sccp.start_strace()
        print('ready to process events...\n')
        for event,content in sccp.waitforevents(events, timeout=30, returnOnMatch=False):
              print("'%s':{%s}" %(event, ','.join("'%s':'%s'" %(key, value) for key,value in content.items())))
    except TIMEOUT:
        print("Connection timed out")
    except EOF:
        print("Disconnect from phone")
    except KeyboardInterrupt:
        print("Interrupted by User")
    except Exception as e:
        print("Exception occured: %s" %e)
        
if __name__ == '__main__':
    main()
    