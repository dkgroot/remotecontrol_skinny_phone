try:
    import sys
    import os
    import re
    import types
    import time
    import requests
    import importlib
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
      self.ssh = None
      self.__dict__.update(iterable, **kwargs)
      self.hostname = hostname
      self.logfile = None
      self.model = self.__import_model()
      self.waiting4events = False
      self.tracing = False
      
    def __del__(self):
      self.disconnect()
               
    def connect(self, timeout=None, maxread=200, clienttimeout=20):
        self.ssh = spawn('./bin/dbclient -y -y -s %s@%s' %(self.username, self.hostname), timeout=timeout, maxread=maxread)
        self.start_logging(self.logfilename)
        self.ssh.expect ('password:',clienttimeout)
        self.ssh.sendline (self.password)

    def __retrieve_device_modelnumber(self):
        url = 'http://%s/DeviceInformationX' %self.hostname
        r = requests.get(url, auth=(self.username, self.password))
        modelnumber = re.search('<modelNumber>(.*)</modelNumber>', r.text)
        if modelnumber:
            return modelnumber.group(1)
        else:
            raise Exception("no modelnumber found in '%s'", r.text)
        
    def __import_model(self):
        self.modelnumber = self.__retrieve_device_modelnumber()
        self.model_series = "none"
        if self.modelnumber.startswith("CP-89"):
            self.model_series = "89xx"
        elif self.modelnumber.startswith("CP-797"):
            self.model_series = "797x"
        else:
            raise Exception("No device model file available for : %s" %self.modelnumber)
        model = importlib.import_module("SccpLogger.models.%s" %self.model_series)  
        return model
        
    def get_modelnumber(self):
        return self.modelnumber

    def start_logging(self, logfilename=None):
        if logfilename != None:
            if self.logfile is None:
                self.logfile = open(self.logfilename,'bw')
            self.ssh.logfile_read = self.logfile
            self.logfilename = logfilename
            
    def stop_logging(self):
        self.ssh.logfile_read = None
        if self.logfile:
            self.logfile.close()
    
    def __parse_expect_reply_list(self, list, clienttimeout=6):
        for entry in list:
            #print("%(expect)s, %(reply)s" %entry)
            if entry['expect']:
                self.ssh.expect(entry['expect'], clienttimeout)
            if entry['reply']:
                self.ssh.sendline(entry['reply'])

    def login(self):
        self.__parse_expect_reply_list(self.model.LOGIN)
    
    def setup_debug(self):   
        self.__parse_expect_reply_list(self.model.SETUP_DEBUG)

    def start_strace(self):
        self.__parse_expect_reply_list(self.model.START_LOGGING)
        self.tracing = True

    def stop_strace(self):
        self.__parse_expect_reply_list(self.model.STOP_LOGGING)
        self.tracing = False

    def reset_debug(self):
        self.__parse_expect_reply_list(self.model.RESET_DEBUG)

    def __generic_event_handler(self, index, child_result_list, returnstr):
        if self.ssh.match.lastgroup:
            content = {k: v.decode("utf-8") for k, v in self.ssh.match.groupdict().items()}
        elif self.ssh.match.lastindex:
            content = {k: v.decode("utf-8") for k,v in enumerate(self.ssh.match.groups())}
        else:
            content = {}
        return returnstr, content
        
    def get_model_event_patternss(self):
        return self.model.EVENT_PATTERNS
    
    def waitforevents(self, events, timeout=None):
        if not self.ssh or not self.ssh.isalive():
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
                    callback_result = self.__generic_event_handler(index, child_result_list, responses[index])
                elif isinstance(responses[index], types.FunctionType):
                    callback_result = responses[index](self.ssh, index, child_result_list)
                if callback_result:
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

    def waitforevent(self, re_pattern, timeout=None):
        if not isinstance(re_pattern, self.ssh.allowed_string_types) and not isinstance(re_pattern, bytes):
            raise Exception('re_pattern needs to be an ascii string or a byte sequence')    
        events = {re.compile(re_pattern):'matched'}
        for event, content in self.waitforevents(events, timeout):
            return event, content
    
    def stopwaiting(self):
        self.waiting4events = False
    
    def disconnect(self):
        if self.ssh and not self.ssh.closed:
            try:
                if self.waiting4events:
                    self.stopwaiting()
                if self.tracing:
                    self.stop_strace()
                self.reset_debug()
                self.stop_logging()
                self.__parse_expect_reply_list(self.model.DISCONNECT)
                self.ssh.close()
            except KeyboardInterrupt:
                exit()
            except Exception as e:
                pass

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
        for event,content in sccp.waitforevents(events, timeout=20):
              print("'%s':{%s}" %(event, ','.join("'%s':'%s'" %(key, value) for key,value in content.items())))
    except TIMEOUT:
        print("Connection timed out")
    except EOF:
        print("Disconnect from phone")
    except KeyboardInterrupt:
        print("Interrupted by User")
    except Exception as e:
        print("Exception occured: %s" %e)
    finally:
        sccp.disconnect()
        