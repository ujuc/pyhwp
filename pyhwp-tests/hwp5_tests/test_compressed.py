# -*- coding: utf-8 -*-
from unittest import TestCase
from hwp5.utils import cached_property


class TestUncompress(TestCase):

    @cached_property
    def original_data(self):
        import os
        return os.urandom(16384)

    @cached_property
    def compressed_data(self):
        import zlib
        return zlib.compress(self.original_data)

    def test_incremental_decode(self):
        compressed_data = self.compressed_data

        from hwp5.compressed import ZLibIncrementalDecoder
        dec = ZLibIncrementalDecoder(wbits=-15)
        data = dec.decode(compressed_data[2:2048])
        data += dec.decode(compressed_data[2048:2048 + 1024])
        data += dec.decode(compressed_data[2048 + 1024:2048 + 1024 + 4096])
        data += dec.decode(compressed_data[2048 + 1024 + 4096:], True)

        self.assertEquals(self.original_data, data)

    def test_decompress(self):
        from StringIO import StringIO

        from hwp5.compressed import decompress_gen
        gen = decompress_gen(StringIO(self.compressed_data[2:]))
        self.assertEquals(self.original_data, ''.join(gen))

        #print '-----'

        from hwp5.compressed import decompress

        f = decompress(StringIO(self.compressed_data[2:]))
        g = StringIO(self.original_data)

        self.assertEquals(f.read(2048), g.read(2048))
        self.assertEquals(f.read(1024), g.read(1024))
        self.assertEquals(f.read(4096), g.read(4096))
        self.assertEquals(f.read(), g.read())
