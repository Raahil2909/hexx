import struct
import zlib


class Chunk:
    def __init__(self, chunk_len, chunk_type, chunk_data, chunk_crc):
        self.chunk_len = chunk_len
        self.chunk_type = chunk_type
        self.chunk_data = chunk_data
        self.chunk_crc = chunk_crc

    def show_chunk(self):
        print(f'{self.chunk_len=}, {self.chunk_type=}, {self.chunk_crc=}')

    def check_crc(self):
        return self.chunk_crc == zlib.crc32(self.chunk_type + self.chunk_data)

    def fix_crc(self):
        self.chunk_crc = zlib.crc32(self.chunk_type + self.chunk_data)


class Png:
    def __init__(self, name):
        self.filename = name
        with open(self.filename, 'rb') as f:
            self.data = f.read()
            f.close()
        self.chunks = []
        self.magic = b''

    def extract_chunks(self):
        self.magic = self.data[:8]
        idx = 8
        while idx < len(self.data):
            chunk_length = struct.unpack(">I", self.data[idx:idx+4])[0]
            chunk_type = self.data[idx+4:idx+8]
            chunk_data = self.data[idx+8:idx+8+chunk_length]
            chunk_crc = struct.unpack(">I", self.data[idx+8+chunk_length:idx+12+chunk_length])[0]
            idx += 12+chunk_length
            self.chunks.append(Chunk(chunk_length, chunk_type, chunk_data, chunk_crc))

            if chunk_type == b'IEND':
                break

    def show_chunks(self):
        for chunk in self.chunks:
            chunk.show_chunk()

    def check_crcs(self):
        good = True
        for chunk in self.chunks:
            if not chunk.check_crc():
                chunk.show_chunk()
                good = False
        if good:
            print('[+] All CRCs are correct')

    def fix_crcs(self):
        self.data = self.magic
        for chunk in self.chunks:
            chunk.fix_crc()
            self.data += struct.pack(">I", chunk.chunk_len)
            self.data += chunk.chunk_type + chunk.chunk_data
            self.data += struct.pack(">I", chunk.chunk_crc)

    def save_back(self):
        with open(self.filename, 'wb') as f:
            f.write(self.data)
            f.close()


p = Png('./testing/ball.png')
p.extract_chunks()
p.check_crcs()
p.fix_crcs()
p.save_back()
