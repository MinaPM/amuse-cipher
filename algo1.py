import hashlib
from bloom_filter import BloomFilter

def encrypt_file(file: bytes, H, prob: float, postamble: bytes = b"") -> BloomFilter:
    """
    Algorithm 1: Encrypt a message/file into a Bloom Filter.
    
    Args:
        file: The data to encrypt (as bytes).
        H: A hash object (e.g., from hashlib) that supports update() and digest().
        prob: The desired false positive probability for the Bloom Filter.
        postamble: Optional postamble bytes to append.
        
    Returns:
        A BloomFilter object containing the encrypted file.
    """
    size = len(file)
    # We use max(1, size + len(postamble)) for max_elements to avoid ValueError for empty inputs
    bf = BloomFilter(max_elements=max(1, size + len(postamble)), error_rate=prob)
    
    for i in range(size):
        # file[i:i+1] gets the single byte at index i as a bytes object
        H.update(file[i:i+1])
        # Note: the BloomFilter library uses 'add', while the pseudocode says 'insert'
        bf.add(H.digest())
        
    for i in range(len(postamble)):
        H.update(postamble[i:i+1])
        bf.add(H.digest())
        
    return bf
