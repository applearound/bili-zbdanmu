import json
import zlib

from bili_zbdanmu.client import DanMuBot
from bili_zbdanmu.constant import ContentTypes, PacketTypes
from bili_zbdanmu.message import Header

import sys
print(sys.path)

def process(header_bytes: bytes, content_bytes: bytes):
    header = Header.from_bytes(header_bytes)
    if header.packet_type == PacketTypes.NOTICE:
        if header.content_type == ContentTypes.UNCOMPRESSED_JSON:
            pass
        elif header.content_type == ContentTypes.COMPRESSED_JSON:
            decompressed_bytes = zlib.decompress(content_bytes)
            cursor = 0
            while cursor != len(decompressed_bytes):
                chunk_header = Header.from_bytes(decompressed_bytes[cursor:cursor + Header.HEADER_LENGTH])
                data = json.loads(decompressed_bytes[cursor + Header.HEADER_LENGTH:cursor + chunk_header.packet_length])
                if data.get('cmd') == 'DANMU_MSG':
                    print(f'{data["info"][2][1]}[{data["info"][2][0]}]: {data["info"][1]}')
                cursor += chunk_header.packet_length
        else:
            print('wired two!')
    elif header.packet_type == PacketTypes.SERVER_HEARTBEAT:
        pass
    elif header.packet_type == PacketTypes.SERVER_LOGIN_RESPONSE:
        pass
    else:
        print('wired!')


if __name__ == '__main__':
    DanMuBot(5050, None).listen()
