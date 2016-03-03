#!/usr/bin/env python3
try:
    import sys
    import os
    import re
    import types
    import time
    from subprocess import Popen, PIPE
    from pexpect import ExceptionPexpect, TIMEOUT, EOF, spawn
    from pprint import pprint
    from SccpLogger import TONES, TONEDIRECTION, OPCODES
except ImportError:
    err = sys.exc_info()[1]
    raise ImportError(str(err) + '''

   A critical module was not found. Probably this operating system does not
   support it. Pexpect is intended for UNIX-like operating systems.''')
class SccpLogger:
    def __init__(self, hostname, iterable=(), **kwargs):
      self.__dict__.update(iterable, **kwargs)
      self.hostname = hostname
      self.waiting4events = False
   
    def connect(self, timeout=None, maxread=200, clienttimeout=20):
        self.ssh = spawn('./dbclient -y -y -s %s@%s' %(self.username, self.hostname), timeout=timeout, maxread=maxread)
        self.start_logging(self.logfile)
        self.ssh.expect ('password:',clienttimeout)
        self.ssh.sendline (self.password)

    def start_logging(self, logfile=None):
        if logfile != None:
            if self.fout is None:
                self.fout = open(self.logfile,'bw')
            self.ssh.logfile_read = self.fout
            self.logfile = logfile

    def stop_logging(self):
        self.ssh.logfile_read = None
        if self.fout:
            self.fout.close()

    def login(self, clienttimeout=2):
        self.ssh.expect ('login:',clienttimeout)
        self.ssh.sendline (self.shelluser)
        self.ssh.expect ('password:',clienttimeout)
        self.ssh.sendline (self.shellpasswd)
    
    def setup_debug(self, clienttimeout=2):   
        self.ssh.expect ('$',clienttimeout)
        self.ssh.sendline('settmask -k')	# stop kernel level logging
        self.ssh.expect ('$',clienttimeout)
        self.ssh.sendline('settmask -s')	# stop process level logging
        self.ssh.expect ('$',clienttimeout)
        self.ssh.sendline('debugsh')
        self.ssh.expect ('$',clienttimeout)
        self.ssh.sendline('jvm logging level NONE')	# stop jvm level logging
        self.ssh.expect ('$',clienttimeout)
        self.ssh.sendline('debug jvm SCCP debug')
        self.ssh.expect ('$',clienttimeout)
        self.ssh.sendline('debug jvm PushService debug')
        self.ssh.expect ('$',clienttimeout)
        self.ssh.sendline('debug jvm XML debug')
        self.ssh.expect ('$',clienttimeout)
        self.ssh.sendline('quit')

    def start_strace(self, clienttimeout=2):
        self.ssh.expect ('$',clienttimeout)
        self.ssh.sendline ('strace')

    def stop_strace(self, clienttimeout=2):
        self.ssh.send('^C')
        self.ssh.expect('$', clienttimeout)

    def generic_event_handler(self, index, child_result_list, returnstr):
        if self.ssh.match.lastgroup:
            content = {k: v.decode("utf-8") for k, v in self.ssh.match.groupdict().items()}
        elif self.ssh.match.lastindex:
            content = {k: v.decode("utf-8") for k,v in enumerate(self.ssh.match.groups())}
        else:
            content = {}
        return returnstr, content
    
    def waitforevents(self, events, timeout=None, returnOnMatch=False):
        if not self.ssh.isalive():
            raise EOF("Not Connected")
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
                    callback_result = self.generic_event_handler(index, child_result_list, responses[index])
                elif isinstance(responses[index], types.FunctionType):
                    callback_result = responses[index](self.ssh, index, child_result_list)
                
                if callback_result:
                    if returnOnMatch:
                        return callback_result
                    else:
                        yield callback_result
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
        self.waiting4events = False
    
    def disconnect(self):
        if not self.ssh.closed:
            if self.waiting4events:
                self.stopwaiting()
            self.stop_strace()
            self.stop_logging()
            self.ssh.sendline('exit')
            self.ssh.close()

    def lookup_opcode(self, opcode):
        return OPCODES[opcode]
        
    def lookup_tone(self, tone):
        return TONES[tone]

    def lookup_tonedirection(self, dir):
        return TONEDIRECTION[dir]

if __name__ == '__main__':
    def handle_read(ssh, index, child_result_list):
       opcode = int(ssh.match.group(2), 16)
       if opcode == 256: # Skip Keepalive
           return None
       else:
           return 'Read', {'Read':sccp.lookup_opcode(opcode),'Length':int(ssh.match.group(1))}

    def handle_write(ssh, index, child_result_list):
       opcode = int(ssh.match.group(2), 16)
       if opcode == 0: # Skip KeepaliveAck
           return None
       else:
           return 'Write', {'Written':sccp.lookup_opcode(opcode),'Length':int(ssh.match.group(1))}

    # just an example of possible matches
    events = {
        re.compile(b'Read Sccp Length: (?P<length>\d+) messageType: (?P<type>0x[0-9a-fA-F]+) avalable:'):handle_read,
        re.compile(b'Writing Sccp Length: (?P<length>\d+) for SCCP MSG: (?P<type>0x[0-9a-fA-F]+)\\n'):handle_write,
        re.compile(b'processSoftkey (?P<SoftkeyIndex>\d) DOWN IN\\n'):'SoftKeyDown',
        re.compile(b'processSoftkey (?P<SoftkeyIndex>\d) DOWN OUT\\n'):'SottKeyUp',
        re.compile(b'callState - CALL STATE IS  =(?P<State>.*)\\n'):'CallState',
    }

    sccp = SccpLogger('10.15.15.205')
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
