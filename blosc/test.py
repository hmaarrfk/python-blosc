import unittest
import ctypes
import blosc

class TestCodec(unittest.TestCase):

    def test_basic_codec(self):
        s = '0123456789'
        c = blosc.compress(s, typesize=1)
        d = blosc.decompress(c)
        self.assertEqual(s, d)

    def test_compress_exceptions(self):
        s = '0123456789'

        self.assertRaises(ValueError, blosc.compress, s, typesize=1, clevel=-1)
        self.assertRaises(ValueError, blosc.compress, s, typesize=1, clevel=10)

        self.assertRaises(ValueError, blosc.compress, 1.0, 1)
        self.assertRaises(ValueError, blosc.compress, ['abc'], 1)

        self.assertRaises(ValueError, blosc.compress,
                'a' * (blosc.BLOSC_MAX_BUFFERSIZE+1), typesize=1)

    def test_compress_ptr_exceptions(self):
        # Make sure we do have a valid address, to reduce the chance of a
        # segfault if we do actually start compressing because the exceptions
        # aren't raised.

        import ctypes
        typesize = 8
        items = 8
        data = [float(i) for i in range(items)]
        Array = ctypes.c_double * items
        array = Array(*data)
        address = ctypes.addressof(array)

        self.assertRaises(ValueError, blosc.compress_ptr, address, items,
                typesize=typesize, clevel=-1)
        self.assertRaises(ValueError, blosc.compress_ptr, address, items,
                typesize=typesize, clevel=10)


        self.assertRaises(TypeError, blosc.compress_ptr, 1.0, items,
                typesize=typesize)
        self.assertRaises(TypeError, blosc.compress_ptr, ['abc'], items,
                typesize=typesize)

        self.assertRaises(ValueError, blosc.compress_ptr, address,
                blosc.BLOSC_MAX_BUFFERSIZE+1, typesize=typesize)

if __name__ == '__main__':
        unittest.main()
