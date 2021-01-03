from __future__ import annotations

import asyncio
import collections
import concurrent
import json

import aiohttp

from message import Header


class DanMuBot:
    @staticmethod
    def normal_process(header_bytes, content_bytes):
        print(header_bytes, content_bytes)

    @staticmethod
    def create_login_data_dict(room_id: int, key: str) -> dict:
        return {
            'uid': 0,
            'roomid': room_id,
            'protover': 2,
            'platform': 'web',
            'clientver': '2.5.11',
            'type': 2,
            'key': key,
        }

    @staticmethod
    def create_header(packet_length: int, content_type: int, packet_type: int) -> Header:
        return Header(packet_length, 16, content_type, packet_type, 1)

    @classmethod
    def build_login_data_bytes(cls: type[DanMuBot], room_id: int, key: str) -> bytes:
        login_data_dict = cls.create_login_data_dict(room_id, key)
        return bytes(json.dumps(login_data_dict, separators=(',', ':')), 'utf-8')

    @classmethod
    def build_login_packet(cls: type[DanMuBot], room_id: int, key: str) -> bytes:
        login_data_bytes = cls.build_login_data_bytes(room_id, key)
        header_bytes = cls.create_header(16 + len(login_data_bytes), 1, 7).to_bytes()
        return header_bytes + login_data_bytes

    GET_DANMU_INFO_URL = 'https://api.live.bilibili.com/xlive/web-room/v1/index/getDanmuInfo'
    GET_DANMU_INFO_HEADERS = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
    }
    HEARTBEAT_BYTES = b'[object Object]'
    HEARTBEAT_PACKET = Header(16 + len(HEARTBEAT_BYTES), 16, 1, 2, 1).to_bytes() + HEARTBEAT_BYTES

    def __init__(self: DanMuBot, room_id: int, handler: collections.abc.Callable[[bytes, bytes], None] = None) -> None:
        self.__room_id: int = room_id
        self.__heartbeat_interval: int = 30
        self.__executor = concurrent.futures.ProcessPoolExecutor()
        self.__handler = handler

    async def __get_danmu_server_token_and_address(
            self: DanMuBot) -> tuple[str, str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.GET_DANMU_INFO_URL,
                    params={
                        'id': self.__room_id,
                        'type': 0
                    },
                    headers=self.GET_DANMU_INFO_HEADERS) as response:
                if response.status != 200:
                    print('无法从哔哩哔哩服务器获取正确的响应')
                elif response.content_type == 'application/json':
                    data = (await response.json())['data']

                    key = data['token']
                    host_list = data['host_list']
                    host = host_list[0]['host']
                    wss_port = host_list[0]['wss_port']
                    return key, f'wss://{host}:{wss_port}/sub'
                else:
                    print('无法解析哔哩哔哩服务器返回的数据')

    async def __listen_to_danmu_server(self: DanMuBot, key: str, danmu_server_address: str):
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(danmu_server_address) as ws:
                await ws.send_bytes(
                    self.build_login_packet(self.__room_id, key))
                loop = asyncio.get_event_loop()
                loop.create_task(self.__send_heartbeat(ws))
                await self.__process_msg(ws)

    async def __process_msg(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        ws.receive
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                self.__executor.submit(self.normal_process if self.__handler is None else self.__handler, msg.data[:Header.HEADER_LENGTH], msg.data[Header.HEADER_LENGTH:])
            else:
                break

    async def __send_heartbeat(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        while True:
            await ws.send_bytes(self.HEARTBEAT_PACKET)
            await asyncio.sleep(self.__heartbeat_interval)

    async def __listen(self: DanMuBot):
        key, address = await self.__get_danmu_server_token_and_address()
        await self.__listen_to_danmu_server(key, address)

    def listen(self: DanMuBot):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__listen())
