#!/usr/bin/env python3
import re
from SccpLogger.SccpLogger import SccpLogger

def main():
    def handle_read(ssh, index, child_result_list):
       if ssh.match:
           opcode = int(ssh.match.group(2), 16)
           if opcode != 256: # Skip Keepalive
               print("Read: %s(%x), length:%d" %(sccp.lookup_opcode(opcode), opcode, int(ssh.match.group(1))))

    def handle_write(ssh, index, child_result_list):
       if ssh.match:
           opcode = int(ssh.match.group(2), 16)
           if opcode != 0: # Skip KeepaliveAck
               print("Written: %s(%x), length:%d" %(sccp.lookup_opcode(opcode), opcode, int(ssh.match.group(1))))

    events = {
        re.compile(b'Read Sccp Length: (?P<length>\d+) messageType: (?P<type>0x[0-9a-fA-F]+) avalable:'):handle_read,
        re.compile(b'Writing Sccp Length: (?P<length>\d+) for SCCP MSG: (?P<type>0x[0-9a-fA-F]+)\\n'):handle_write,
        
        # device control
        re.compile(b'\[DevRecSm\]: execute(?P<execute>.*), CurState=(?P<curstate>.*)\\n'):'DevStateChange',
        re.compile(b'processSoftkey (?P<SoftkeyIndex>\d) DOWN IN\\n'):'SoftKeyDown',
        re.compile(b'processSoftkey (?P<SoftkeyIndex>\d) DOWN OUT\\n'):'SottKeyUp',
        re.compile(b'Received SOFT: (?P<SoftkeyIndex>\d)\\n'):'SoftKeyPressed',
        re.compile(b'setAudioPath \((?P<Path>.*)\)\\n'):'AudioPath',		# HANDSET / SPEAKER / NONE
        re.compile(b'DisplayTask:\? - (?P<State1>.*)=(?P<Active1>[false|true])\\n'):'DisplayState',
        re.compile(b'DisplayTask:\? - Active Call Count: (?P<Num>\d)\\n'):'ActiveCallCount',
        re.compile(b'DisplayTask:\? - (?P<State1>.*)=(?P<Active1>[false|true]) (?P<State2>.*)=(?P<Active2>[false|true])\\n'):'DisplayStateRunning',
        re.compile(b'InputManager:\? - Received DTMF: (?P<Num>\d+)\\n'):'ReceivedDTMF',
        re.compile(b'Notifying model of controller with name Line-(?P<LineNum>\d+)  event \d+\\n'):'LineUsed',
        re.compile(b'setOverviewCallAndLineState - DN=(?P<DN>\d+) lineState=(?P<LineState>.*) old lineWeight=.* new lineWeight=.*\\n'):'',
        re.compile(b'setText \( "(?P<Text>.*)" \)\\n'):'StatusPrompt',		# Ring out / Call Proceed / Connected / Your current options
        
        # call control
        re.compile(b'Tone-AUDIBLE FEEDBACK: (?P<State>.*):\(ToneType: (?P<Type>\d+), ToneDir: (?P<Direction>\d+)\)\\n'):'tone',
        re.compile(b'callState - CALL STATE IS(?P<State>\S*)\\n'):'callstate',
        re.compile(b'Call View: Call-(?P<CallNum>\d+) draw\\n'):'CallView',
        
        # rtp flow
        re.compile(b'MediaTermination_open(?P<Gress>.*)\\n'):'mediatermination',
        re.compile(b'STREAM- (?P<Gress>.*)\\n'):'stream',
        re.compile(b'(?P<ORC>In ORC Bit Rate.*)\\n'):'openreceivechannel',
        re.compile(b'(?P<SMT>In SMT Bit Rate.*)\\n'):'startmediatransmission',
        re.compile(b'openEgressChannel, multicastListenIp=(?P<MultiCastIP>.*), localPort=(?P<Port>\d+), mediaPayloadType=(?P<Type>\d)\\n'):'openEgressChannel',
        re.compile(b'openIngressChannel, remoteIpAddr=(?P<IP>.*), remotePort=(?P<Port>\d+), mediaPayloadType=(?P<Type>\d)\\n'):'openIngressChannel',
    }

    sccp = SccpLogger('10.15.15.205')
    sccp.connect()
    sccp.waitforevents(events)

if __name__ == '__main__':
    main()