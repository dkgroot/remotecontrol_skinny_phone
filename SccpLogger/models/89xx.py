SERIES = "89xx"
LOGIN = []

SETUP_DEBUG = [
    {'expect':r'\[CP-8945\]','reply': 'spy CMM 0\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy WEBLITE 2\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy ACCU 2 \r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy TSTN 2\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy PSCCP 0\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy PFS 0\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy SECD 0\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy CLOG 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy TUIU 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy CMMT 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy PXMAN 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy EHS 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy AWBU 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy URL  3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy DLMM 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy AMXU 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy SIP  3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy CUVA 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy AMMU 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy VVMU 3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy VPN  3\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'debug telephony verbose\r\n'},
]

RESET_DEBUG = [
    {'expect':None,'reply': 'debug telephony default\r\n'},
    {'expect':r'\[CP-8945\]','reply': 'spy default\r\n'},
]

START_LOGGING = []

STOP_LOGGING = [
]

DISCONNECT = [
    {'expect':None,'reply': 'exit\r\n'},
]

EVENT_PATTERNS = {
}
