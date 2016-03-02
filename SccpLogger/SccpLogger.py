#!/usr/bin/env python3
try:
    import sys
    import os
    import re
    import types
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
   
    def connect(self, timeout=None, maxread=200):
      try:
        print('connecting via ssh to %s...' %self.hostname)
        self.ssh = spawn('./dbclient -y -y -s %s@%s' %(self.username, self.hostname), timeout=timeout, maxread=maxread)
        if self.logfile != None:
            self.fout = open(self.logfile,'bw')
            self.ssh.logfile_read = self.fout
            print ("sending output to %s" %self.logfile)
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
            print ("'%s':{%s}" %(returnstr, ','.join("'%s':'%s'" %(key,value.decode("utf-8")) for key,value in self.ssh.match.groupdict().items())))
        elif self.ssh.match and self.ssh.match.lastindex:
            print ("'%s':[%s]" %(returnstr, ','.join(repr(match.decode("utf-8")) for match in self.ssh.match.groups())))
        else:
            print ("'%s'" %(returnstr))
    
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
        if self.fout:
            fout.close()

    def lookup_opcode(self, opcode):
        return OPCODES[opcode]
        
    def lookup_tone(self, tone):
        return TONES[tone]

    def lookup_tonedirection(self, dir):
        return TONEDIRECTION[dir]

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

    # just an example of possible matches
    events = {
        re.compile(b'Read Sccp Length: (?P<length>\d+) messageType: (?P<type>0x[0-9a-fA-F]+) avalable:'):handle_read,
        re.compile(b'Writing Sccp Length: (?P<length>\d+) for SCCP MSG: (?P<type>0x[0-9a-fA-F]+)\\n'):handle_write,
        re.compile(b'\[DevRecSm\]: execute(?P<execute>.*), CurState=(?P<curstate>.*)\\n'):'DevStateChange',
        re.compile(b'processSoftkey (?P<SoftkeyIndex>\d) DOWN IN\\n'):'SoftKeyDown',
        re.compile(b'processSoftkey (?P<SoftkeyIndex>\d) DOWN OUT\\n'):'SottKeyUp',
    }

    sccp = SccpLogger('10.15.15.205')
    sccp.connect()
    sccp.waitforevents(events)
