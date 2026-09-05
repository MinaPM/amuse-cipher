import unittest
import hashlib
from algo1 import encrypt_file
from algo2 import decrypt_file


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.message = b"test message"
        self.postamble = b"END"
        self.prob = 0.001

    def test_encrypt_decrypt_basic(self):
        bf = encrypt_file(self.message, hashlib.sha256(),
                          self.prob, self.postamble)
        self.assertIsNotNone(bf)

        decrypted = decrypt_file(bf, hashlib.sha256(),
                                 len(self.message), self.postamble)
        self.assertEqual(decrypted, self.message)

    def test_encrypt_decrypt_empty_message(self):
        message = b""
        bf = encrypt_file(message, hashlib.sha256(), self.prob, self.postamble)

        decrypted = decrypt_file(bf, hashlib.sha256(),
                                 len(message), self.postamble)
        self.assertEqual(decrypted, message)

    def test_encrypt_decrypt_empty_postamble(self):
        postamble = b""
        bf = encrypt_file(self.message, hashlib.sha256(), self.prob, postamble)

        decrypted = decrypt_file(bf, hashlib.sha256(),
                                 len(self.message), postamble)
        self.assertEqual(decrypted, self.message)

    def test_encrypt_decrypt_different_hash(self):
        # Using md5 instead of sha256
        bf = encrypt_file(self.message, hashlib.md5(),
                          self.prob, self.postamble)
        decrypted = decrypt_file(
            bf, hashlib.md5(), len(self.message), self.postamble)
        self.assertEqual(decrypted, self.message)

    def test_wrong_size(self):
        bf = encrypt_file(self.message, hashlib.sha256(),
                          self.prob, self.postamble)

        # Supplying incorrect size - might return None or something incorrect
        decrypted = decrypt_file(bf, hashlib.sha256(), len(
            self.message) + 1, self.postamble)
        self.assertNotEqual(decrypted, self.message)

    def test_wrong_postamble(self):
        bf = encrypt_file(self.message, hashlib.sha256(),
                          self.prob, self.postamble)

        decrypted = decrypt_file(bf, hashlib.sha256(),
                                 len(self.message), b"WRONG")
        self.assertIsNone(decrypted)

    def test_wrong_hash_algorithm_for_decryption(self):
        bf = encrypt_file(self.message, hashlib.sha256(),
                          self.prob, self.postamble)

        decrypted = decrypt_file(
            bf, hashlib.md5(), len(self.message), self.postamble)
        self.assertIsNone(decrypted)

    def test_corrupted_bloom_filter(self):
        bf = encrypt_file(self.message, hashlib.sha256(),
                          self.prob, self.postamble)
        
        # Corrupt the Bloom Filter data by zeroing out part of the underlying array
        if hasattr(bf, 'backend') and hasattr(bf.backend, 'array_'):
            if len(bf.backend.array_) > 0:
                bf.backend.array_[0] = 0
                
        decrypted = decrypt_file(bf, hashlib.sha256(),
                                 len(self.message), self.postamble)
        
        # Decryption should fail to find the correct path and return None
        self.assertIsNone(decrypted)


if __name__ == "__main__":
    unittest.main()
