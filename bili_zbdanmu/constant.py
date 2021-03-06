from enum import Enum, IntEnum


class ContentTypes(IntEnum):
    UNCOMPRESSED_JSON = 0
    HEARTBEAT = 1
    COMPRESSED_JSON = 2


class PacketTypes(IntEnum):
    CLIENT_HEARTBEAT = 2
    SERVER_HEARTBEAT = 3
    NOTICE = 5
    CLIENT_LOGIN_REQUEST = 7
    SERVER_LOGIN_RESPONSE = 8


class Commands(Enum):
    DANMU_MSG = 'DANMU_MSG'
    SEND_GIFT = 'SEND_GIFT'
    WELCOME = 'WELCOME'
    WELCOME_GUARD = 'WELCOME_GUARD'
    SYS_MSG = 'SYS_MSG'
    PREPARING = 'PREPARING'
    LIVE = 'LIVE'
    INTERACT_WORD = 'INTERACT_WORD'
    ROOM_BANNER = 'ROOM_BANNER'
    COMBO_SEND = 'COMBO_SEND'
    ENTRY_EFFECT = 'ENTRY_EFFECT'
    ONLINERANK = 'ONLINERANK'
    SUPER_CHAT_MESSAGE = 'SUPER_CHAT_MESSAGE'
    ACTIVITY_BANNER_UPDATE_V2 = 'ACTIVITY_BANNER_UPDATE_V2'
    GUARD_BUY = 'GUARD_BUY'
    ROOM_REAL_TIME_MESSAGE_UPDATE = 'ROOM_REAL_TIME_MESSAGE_UPDATE'
    PANEL = 'PANEL'
    USER_TOAST_MSG = 'USER_TOAST_MSG'
    SUPER_CHAT_MESSAGE_JPN = 'SUPER_CHAT_MESSAGE_JPN'
    NOTICE_MSG = 'NOTICE_MSG'
