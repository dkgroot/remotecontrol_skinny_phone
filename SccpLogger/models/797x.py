SERIES = "797x"

_shelluser = 'default'
_shellpasswd = 'user'

LOGIN = [
    {'expect':'login:','reply':_shelluser},
    {'expect':'password:','reply':_shellpasswd},
]

SETUP_DEBUG = [
    {'expect':'$','reply': 'settmask -k'},	# stop kernel level logging
    {'expect':'$','reply': 'settmask -s'},	# stop process level logging
    {'expect':'$','reply': 'debugsh'},
    {'expect':'$','reply': 'jvm logging level NONE'},	# stop jvm level logging
    {'expect':'$','reply': 'debug jvm SCCP debug'},
    {'expect':'$','reply': 'debug jvm PushService debug'},
    {'expect':'$','reply': 'debug jvm XML debug'},
    {'expect':'$','reply': 'quit'},
]

RESET_DEBUG = [
    {'expect':'$','reply': 'jvm logging level NONE'},
    {'expect':'$','reply': 'settmask -k'},
    {'expect':'$','reply': 'settmask -s'}, 
]

START_LOGGING = [
    {'expect':'$','reply': 'strace'}
]

STOP_LOGGING = [
    {'expect':None,'reply': '^C'},
    {'expect':'$','reply':None},
]

DISCONNECT = [
    {'expect':None,'reply': '^C'},
    {'expect':None,'reply': 'exit'},
]

EVENT_PATTERNS = {
    b'Read Sccp Length: (?P<length>\d+) messageType: (?P<type>0x[0-9a-fA-F]+) avalable:',
    b'Writing Sccp Length: (?P<length>\d+) for SCCP MSG: (?P<type>0x[0-9a-fA-F]+)\\n',
    
    # device control
    b'processSoftkey (?P<SoftkeyIndex>\d) DOWN IN\\n',
    b'processSoftkey (?P<SoftkeyIndex>\d) DOWN OUT\\n',
    b'Received SOFT: (?P<SoftkeyIndex>\d)\\n',
    b'setAudioPath \((?P<Path>.*)\)\\n',								# HANDSET / SPEAKER / NONE
    b'DisplayTask:\? - Active Call Count: (?P<Num>\d)\\n',
    b'DisplayTask:\? - ([a-zA-Z]+)=(true|false) ([a-zA-Z]+)=(true|false)\\n',
    b'DisplayTask:\? - ([a-zA-Z]+)=(true|false)\\n',
    b'InputManager:\? - Received DTMF: (?P<Num>\d+)\\n',
    b'Notifying model of controller with name Line-(?P<LineNum>\d+)  event \d+\\n',
    b'setOverviewCallAndLineState - DN=(?P<DN>\d+) lineState=(?P<LineState>.*) old lineWeight=.* new lineWeight=.*\\n',
    b'setText \( "(?P<Text>.*)" \)\\n',									# Ring out / Call Proceed / Connected / Your current options
    
    # call control
    b'Tone-AUDIBLE FEEDBACK: (?P<State>.*):\(ToneType: (?P<Type>\d+), ToneDir: (?P<Direction>\d+)\)\\n',
    b'callState - CALL STATE IS  =(?P<State>.*)\\n',
    b'Call View: Call-(?P<CallNum>\d+) draw\\n',
    b'processSoftkey (?P<SoftKey>\d) (?P<UpDown>UP|DOWN) (?P<InOut>IN|OUT)\\n',
    
    # rtp flow
    b'MediaTermination_open(?P<Gress>.*)\\n',
    b'STREAM- (?P<Gress>.*)\\n',
    b'(?P<ORC>In ORC Bit Rate.*)\\n',
    b'(?P<SMT>In SMT Bit Rate.*)\\n',
    b'openEgressChannel, multicastListenIp=(?P<MultiCastIP>.*), localPort=(?P<Port>\d+), mediaPayloadType=(?P<Type>\d)\\n',
    b'openIngressChannel, remoteIpAddr=(?P<IP>.*), remotePort=(?P<Port>\d+), mediaPayloadType=(?P<Type>\d)\\n',
}
