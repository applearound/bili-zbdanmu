from __future__ import annotations

import collections
import struct


class Header:
    header_struct = struct.Struct('!IHHII')
    HEADER_LENGTH: int = header_struct.size
    PACK_HEADER: collections.abc.Callable[[...], bytes] = header_struct.pack
    UNPACK_HEADER: collections.abc.Callable[[bytes], tuple[...]] = header_struct.unpack

    def __init__(
        self: Header,
        packet_length: int,
        header_length: int,
        content_type: int,
        packet_type: int,
        reserved: int
    ) -> None:
        self.packet_length: int = packet_length
        self.header_length: int = header_length
        self.content_type: int = content_type
        self.packet_type: int = packet_type
        self.reserved: int = reserved

    def __repr__(self: Header):
        return f'Header[packet_length={self.packet_length}, header_length={self.header_length}, content_type={self.content_type}, packet_type={self.packet_type}, reserved={self.reserved}]'

    def to_bytes(self: Header):
        return self.PACK_HEADER(self.packet_length, self.header_length,
                                self.content_type, self.packet_type,
                                self.reserved)

    @classmethod
    def from_bytes(cls: type[Header], header_bytes: bytes) -> Header:
        return cls(*cls.UNPACK_HEADER(header_bytes))
