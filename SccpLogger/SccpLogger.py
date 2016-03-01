#!/usr/bin/env python3
try:
    import sys
    import os
    import re
    import types
    from subprocess import Popen, PIPE
    from pexpect import ExceptionPexpect, TIMEOUT, EOF, spawn
    from pprint import pprint
except ImportError:
    err = sys.exc_info()[1]
    raise ImportError(str(err) + '''

   A critical module was not found. Probably this operating system does not
   support it. Pexpect is intended for UNIX-like operating systems.''')
   
class SccpLogger:
    opcodes = {
        0x0000: "KeepAlive", 0x0001: "Register", 0x0002: "IpPort", 0x0003: "KeypadButton", 0x0004: "EnblocCall", 0x0005: "Stimulus", 0x0006: "OffHook", 0x0007: "OnHook",
        0x0008: "HookFlash", 0x0009: "ForwardStatReq", 0x000A: "SpeedDialStatReq", 0x000B: "LineStatReq", 0x000C: "ConfigStatReq", 0x000D: "TimeDateReq", 0x000E: "ButtonTemplateReq",
        0x000F: "VersionReq", 0x0010: "CapabilitiesRes", 0x0011: "MediaPortList", 0x0012: "ServerReq", 0x0020: "Alarm", 0x0021: "MulticastMediaReceptionAck", 0x0022: "OpenReceiveChannelAck",
        0x0023: "ConnectionStatisticsRes", 0x0024: "OffHookWithCgpn", 0x0025: "SoftKeySetReq", 0x0026: "SoftKeyEvent", 0x0027: "Unregister", 0x0028: "SoftKeyTemplateReq",
        0x0029: "RegisterTokenRequest", 0x002A: "MediaTransmissionFailure", 0x002B: "HeadsetStatus", 0x002C: "MediaResourceNotification", 0x002D: "RegisterAvailableLines",
        0x002E: "DeviceToUserData", 0x002F: "DeviceToUserDataResponse", 0x0030: "UpdateCapabilities", 0x0031: "OpenMultiMediaReceiveChannelAck", 0x0032: "ClearConference",
        0x0033: "ServiceURLStatReq", 0x0034: "FeatureStatReq", 0x0035: "CreateConferenceRes", 0x0036: "DeleteConferenceRes", 0x0037: "ModifyConferenceRes", 0x0038: "AddParticipantRes",
        0x0039: "AuditConferenceRes", 0x0040: "AuditParticipantRes", 0x0041: "DeviceToUserDataVersion1", 0x0042: "DeviceToUserDataResponseVersion1", 0x0043: "UpdateCapabilitiesV2",
        0x0044: "UpdateCapabilitiesV3", 0x0045: "PortResponse", 0x0046: "QoSResvNotify", 0x0047: "QoSErrorNotify", 0x0048: "SubscriptionStatReq", 0x0049: "AccessoryStatus",
        0x004A: "MediaPathCapability", 0x004C: "MwiNotification", 0x0081: "RegisterAck", 0x0082: "StartTone", 0x0083: "StopTone", 0x0085: "SetRinger", 0x0086: "SetLamp",
        0x0087: "SetHkFDetect", 0x0088: "SetSpeakerMode", 0x0089: "SetMicroMode", 0x008A: "StartMediaTransmission", 0x008B: "StopMediaTransmission", 0x008C: "StartMediaReception",
        0x008D: "StopMediaReception", 0x008F: "CallInfo", 0x0090: "ForwardStat", 0x0091: "SpeedDialStat", 0x0092: "LineStat", 0x0093: "ConfigStat", 0x0094: "DefineTimeDate",
        0x0095: "StartSessionTransmission", 0x0096: "StopSessionTransmission", 0x0097: "ButtonTemplate", 0x0098: "Version", 0x0099: "DisplayText", 0x009A: "ClearDisplay",
        0x009B: "CapabilitiesReq", 0x009C: "EnunciatorCommand", 0x009D: "RegisterReject", 0x009E: "ServerRes", 0x009F: "Reset", 0x0100: "KeepAliveAck", 0x0101: "StartMulticastMediaReception",
        0x0102: "StartMulticastMediaTransmission", 0x0103: "StopMulticastMediaReception", 0x0104: "StopMulticastMediaTransmission", 0x0105: "OpenReceiveChannel", 0x0106: "CloseReceiveChannel",
        0x0107: "ConnectionStatisticsReq", 0x0108: "SoftKeyTemplateRes", 0x0109: "SoftKeySetRes", 0x0110: "SelectSoftKeys", 0x0111: "CallState", 0x0112: "DisplayPromptStatus",
        0x0113: "ClearPromptStatus", 0x0114: "DisplayNotify", 0x0115: "ClearNotify", 0x0116: "ActivateCallPlane", 0x0117: "DeactivateCallPlane", 0x0118: "UnregisterAck",
        0x0119: "BackSpaceReq", 0x011A: "RegisterTokenAck", 0x011B: "RegisterTokenReject", 0x011C: "StartMediaFailureDetection", 0x011D: "DialedNumber", 0x011D: "DialedNumber",
        0x011E: "UserToDeviceData", 0x011F: "FeatureStat", 0x0120: "DisplayPriNotify", 0x0121: "ClearPriNotify", 0x0122: "StartAnnouncement", 0x0123: "StopAnnouncement",
        0x0124: "AnnouncementFinish", 0x0127: "NotifyDtmfTone", 0x0128: "SendDtmfTone", 0x0129: "SubscribeDtmfPayloadReq", 0x012A: "SubscribeDtmfPayloadRes", 0x012B: "SubscribeDtmfPayloadErr",
        0x012C: "UnSubscribeDtmfPayloadReq", 0x012D: "UnSubscribeDtmfPayloadRes", 0x012E: "UnSubscribeDtmfPayloadErr", 0x012F: "ServiceURLStat", 0x0130: "CallSelectStat",
        0x0131: "OpenMultiMediaChannel", 0x0132: "StartMultiMediaTransmission", 0x0133: "StopMultiMediaTransmission", 0x0134: "MiscellaneousCommand", 0x0135: "FlowControlCommand",
        0x0136: "CloseMultiMediaReceiveChannel", 0x0137: "CreateConferenceReq", 0x0138: "DeleteConferenceReq", 0x0139: "ModifyConferenceReq", 0x013A: "AddParticipantReq",
        0x013B: "DropParticipantReq", 0x013C: "AuditConferenceReq", 0x013D: "AuditParticipantReq", 0x013F: "UserToDeviceDataVersion1", 0x0140: "VideoDisplayCommand",
        0x0141: "FlowControlNotify", 0x0142: "ConfigStatDynamic", 0x0143: "DisplayDynamicNotify", 0x0144: "DisplayDynamicPriNotify", 0x0145: "DisplayDynamicPromptStatus",
        0x0146: "FeatureStatDynamic", 0x0147: "LineStatDynamic", 0x0148: "ServiceURLStatDynamic", 0x0149: "SpeedDialStatDynamic", 0x014A: "CallInfoDynamic", 0x014B: "PortRequest",
        0x014C: "PortClose", 0x014D: "QoSListen", 0x014E: "QoSPath", 0x014F: "QoSTeardown", 0x0150: "UpdateDSCP", 0x0151: "QoSModify", 0x0152: "SubscriptionStat",
        0x0153: "Notification", 0x0154: "StartMediaTransmissionAck", 0x0155: "StartMultiMediaTransmissionAck", 0x0156: "CallHistoryDisposition", 0x0157: "LocationInfo",
        0x0158: "MwiResponse", 0x0159: "ExtensionDeviceCaps", 0x015A: "XMLAlarm", 0x015E: "CallCountReq", 0x015F: "CallCountResp", 0x0160: "RecordingStatus", 0x8000: "SPCPRegisterTokenRequest",
        0x8100: "SPCPRegisterTokenAck", 0x8101: "SPCPRegisterTokenReject", 0xFF00: "UnknownVG", 0xFF02: "SPCPPlatformInfoGetReq", 0xFF03: "SPCPPlatformInfoGetRsp", 0xFF04: "SPCPPlatformInfoGetRej",
    }

    def __init__(self, hostname, username='cisco', password='cisco', shelluser='default', shellpasswd='user'):
      self.hostname = hostname
      self.username = username
      self.password = password
      self.shelluser = shelluser
      self.shellpasswd = shellpasswd
      self.waiting4events = False
    
    def connect(self, timeout=None, maxread=200):
      try:
        print('connecting via ssh to %s...' %self.hostname)
        self.ssh = spawn('./dbclient -y -y -s %s@%s' %(self.username, self.hostname), timeout=timeout, maxread=maxread)
        self.ssh.expect ('password:')
        self.ssh.sendline (self.password)
        print('connected')
        self.ssh.expect ('login:')
        self.ssh.sendline (self.shelluser)
        self.ssh.expect ('password:')
        self.ssh.sendline (self.shellpasswd)
        print('logged in to shell. setting up debug environment...')
        self.ssh.expect ('$')
        self.ssh.sendline('settmask -k')	# stop kernel level logging
        self.ssh.expect ('$')
        self.ssh.sendline('settmask -s')	# stop process level logging
        self.ssh.expect ('$')
        self.ssh.sendline('debugsh')
        self.ssh.expect ('$')
        self.ssh.sendline('jvm logging level NONE')	# stop jvm level logging
        self.ssh.expect ('$')
        self.ssh.sendline('debug jvm SCCP debug')
        self.ssh.expect ('$')
        self.ssh.sendline('debug jvm PushService debug')
        self.ssh.expect ('$')
        self.ssh.sendline('debug jvm XML debug')
        self.ssh.expect ('$')
        self.ssh.sendline('quit')
        print('starting strace...')
        self.ssh.expect ('$')
        self.ssh.sendline ('strace')
        print('ready to process events...\n')
      except ExceptionPexpect as e:
        print('ssh connection failed')
        print(e)

    def handle_returnstr(self, index, child_result_list, returnstr):
        if self.ssh.match and self.ssh.match.lastgroup:
            print ("%s:{%s}" %(returnstr, ','.join("'%s':'%s'" %(key,value.decode("utf-8")) for key,value in self.ssh.match.groupdict().items())))
        elif self.ssh.match and self.ssh.match.lastindex:
            print ("%s:[%s]" %(returnstr, ','.join(repr(match.decode("utf-8")) for match in self.ssh.match.groups())))
        else:
            print ("%s" %(returnstr))
    
    def waitforevents(self, events, timeout=None):
        if not self.ssh.isalive():
            print('not connected')
            return
        patterns = list(events.keys())
        responses = list(events.values())
        compiled_pattern_list = self.ssh.compile_pattern_list(patterns)
        child_result_list = []
        self.waiting4events = True
        print("waiting4events...")
        while self.waiting4events:
            try:
                index = self.ssh.expect_list(compiled_pattern_list, timeout)
                if isinstance(responses[index], self.ssh.allowed_string_types):
                    callback_result = self.handle_returnstr(index, child_result_list, responses[index])
                if isinstance(responses[index], types.FunctionType):
                    callback_result = responses[index](self.ssh, index, child_result_list)
                sys.stdout.flush()
            except TIMEOUT:
                child_result_list.append(self.ssh.before)
                break
            except EOF:
                child_result_list.append(self.ssh.before)
                break
            except KeyboardInterrupt:
                self.disconnect()
                break
            child_result = self.ssh.string_type().join(child_result_list)
    
    def stopwaiting(self):
        print("stopped waiting4events")
        self.waiting4events = False
    
    def disconnect(self):
        if not self.ssh.closed:
            if self.waiting4events:
                self.stopwaiting()
            self.ssh.send('^C')
            self.ssh.expect('$')
            self.ssh.sendline('exit')
            self.ssh.close()

    def lookup_opcode(self, opcode):
        return self.opcodes[opcode]

if __name__ == '__main__':
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
