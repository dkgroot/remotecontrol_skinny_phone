__version__ = '0.1'
__revision__ = '0'
__all__ = ['SccpLogger', '__version__', '__revision__']

OPCODES = {
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
        0x8100: "SPCPRegisterTokenAck", 0x8101: "SPCPRegisterTokenReject", 0xFF00: "UnknownVG", 0xFF02: "SPCPPlatformInfoGetReq", 0xFF03: "SPCPPlatformInfoGetRsp", 0xFF04: "SPCPPlatformInfoGetRej"
}

TONES = {
	0x00:"SILENCE",0x01:"DTMF1",0x02:"DTMF2",0x03:"DTMF3",0x04:"DTMF4",0x05:"DTMF5",0x06:"DTMF6",0x07:"DTMF7",0x08:"DTMF8",0x09:"DTMF9",0x0A:"DTMF0",0x0E:"DTMFSTAR",
	0x0F:"DTMFPOUND",0x10:"DTMFA",0x11:"DTMFB",0x12:"DTMFC",0x13:"DTMFD",0x21:"INSIDEDIALTONE",0x22:"OUTSIDEDIALTONE",0x23:"LINEBUSYTONE",0x24:"ALERTINGTONE",
	0x25:"REORDERTONE",0x26:"RECORDERWARNINGTONE",0x27:"RECORDERDETECTEDTONE",0x28:"REVERTINGTONE",0x29:"RECEIVEROFFHOOKTONE",0x2A:"PARTIALDIALTONE",0x2B:"NOSUCHNUMBERTONE",
	0x2C:"BUSYVERIFICATIONTONE",0x2D:"CALLWAITINGTONE",0x2E:"CONFIRMATIONTONE",0x2F:"CAMPONINDICATIONTONE",0x30:"RECALLDIALTONE",0x31:"ZIPZIP",0x32:"ZIP",0x33:"BEEPBONK",
	0x34:"MUSICTONE",0x35:"HOLDTONE",0x36:"TESTTONE",0x37:"DTMONITORWARNINGTONE",0x40:"ADDCALLWAITING",0x41:"PRIORITYCALLWAIT",0x42:"RECALLDIAL",0x43:"BARGIN",0x44:"DISTINCTALERT",
	0x45:"PRIORITYALERT",0x46:"REMINDERRING",0x47:"PRECEDENCE_RINGBACK",0x48:"PREEMPTIONTONE",0x50:"MF1",0x51:"MF2",0x52:"MF3",0x53:"MF4",0x54:"MF5",0x55:"MF6",0x56:"MF7",
	0x57:"MF8",0x58:"MF9",0x59:"MF0",0x5A:"MFKP1",0x5B:"MFST",0x5C:"MFKP2",0x5D:"MFSTP",0x5E:"MFST3P",0x5F:"MILLIWATT",0x60:"MILLIWATTTEST",0x61:"HIGHTONE",0x62:"FLASHOVERRIDE",
	0x63:"FLASH",0x64:"PRIORITY",0x65:"IMMEDIATE",0x66:"PREAMPWARN",0x67:"2105HZ",0x68:"2600HZ",0x69:"440HZ",0x6A:"300HZ",0x77:"MLPP_PALA",0x78:"MLPP_ICA",0x79:"MLPP_VCA",
	0x7A:"MLPP_BPA",0x7B:"MLPP_BNEA",0x7C:"MLPP_UPA",0x7F:"NOTONE",0x80:"MEETME_GREETING",0x81:"MEETME_NUMBER_INVALID",0x82:"MEETME_NUMBER_FAILED",0x83:"MEETME_ENTER_PIN",
	0x84:"MEETME_INVALID_PIN",0x85:"MEETME_FAILED_PIN",0x86:"MEETME_CFB_FAILED",0x87:"MEETME_ENTER_ACCESS_CODE",0x88:"MEETME_ACCESS_CODE_INVALID",0x89:"MEETME_ACCESS_CODE_FAILED"
}
