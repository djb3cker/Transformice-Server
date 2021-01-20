import struct

class ByteArray:
    def __init__(self, data=b""):
        if type(data) == bytes:
            self.bytes = data
        elif type(data) == str:
            self.bytes = data.encode()
        else:
            self.bytes = b""

    def read(self, length: int):
        value = self.bytes[:length]
        self.bytes = self.bytes[length:]
        return value

    def write(self, data: bytes):
        global bytes
        self.bytes += bytes(data)
        return self

    def writeBoolean(self, data: bool):
        self.writeByte(int(data))
        return self

    def writeByte(self, data: int):
        self.bytes += struct.pack('!b', int(data))
        return self

    def writeUnsignedByte(self, data: int):
        self.bytes += struct.pack('!B', int(data))
        return self

    def writeBytes(self, data: bytes):
        self.bytes += data
        return self

    def writeShort(self, data: int):
        self.bytes += struct.pack('!h', int(data))
        return self

    def writeUnsignedShort(self, data: int):
        self.bytes += struct.pack('!H', int(data))
        return self

    def writeInt(self, data: int):
        if data < 0:
            self.bytes += struct.pack('!i', int(data))
        else:
            self.bytes += struct.pack('!I', int(data))
        return self

    def writeLong(self, data: int):
        self.bytes += struct.pack('!Q', int(data))
        return self

    def writeUTF(self, data: str):
        if type(data) == str:
            data = data.encode()
        length = len(data)
        self.bytes += struct.pack('!H', length)
        self.bytes += data
        return self

    def readBoolean(self):
        data = struct.unpack('!?', self.bytes[:1])[0]
        self.bytes = self.bytes[1:]
        return data

    def readByte(self):
        data = struct.unpack('!b', self.bytes[:1])[0]
        self.bytes = self.bytes[1:]
        return data

    def readUnsignedByte(self):
        data = struct.unpack('!B', self.bytes[:1])[0]
        self.bytes = self.bytes[1:]
        return data

    def readBytes(self, length: __init__):
        data = self.bytes[:length]
        self.bytes = self.bytes[length:]
        return data

    def readShort(self):
        data = struct.unpack('!h', self.bytes[:2])[0]
        self.bytes = self.bytes[2:]
        return data

    def readUnsignedShort(self):
        data = struct.unpack('!H', self.bytes[:2])[0]
        self.bytes = self.bytes[2:]
        return data

    def readInt(self):
        data = struct.unpack('!i', self.bytes[:4])[0]
        self.bytes = self.bytes[4:]
        return data

    def readUnsignedInt(self):
        data = struct.unpack('!I', self.bytes[:4])[0]
        self.bytes = self.bytes[4:]
        return data

    def readLong(self):
        data = struct.unpack('!Q', self.bytes[:8])[0]
        self.bytes = self.bytes[8:]
        return data

    def readUTF(self):
        length = struct.unpack('!H', self.bytes[:2])[0]
        data = self.bytes[2:(length + 2)]
        self.bytes = self.bytes[(2 + length):]
        return data.decode('utf-8', 'ignore')

    def toByteArray(self):
        return self.bytes

    def clear(self):
        self.bytes = b''
        return self

    def length(self):
        return len(self.bytes)

    def bytesAvailable(self):
        return len(self.bytes) > 0