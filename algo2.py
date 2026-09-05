from collections import deque
from bloom_filter import BloomFilter


def decrypt_file(bf: BloomFilter, H, size: int, postamble: bytes, progress_callback=None) -> bytes | None:
    """
    Algorithm 2: Decrypt a message/file from a Bloom Filter.

    Args:
        bf: The BloomFilter containing the encrypted file.
        H: A hash object (e.g., from hashlib) matching the one used for encryption.
        size: The known size of the original file.
        postamble: The postamble bytes used to verify the correct message.
        progress_callback: Optional callable taking (current_prefix, target_size) to report progress.

    Returns:
        The decrypted file as bytes, or None if decryption fails.
    """
    # Start from an empty prefix and initialize a BFS queue
    # The queue stores tuples of (hash_state, prefix_bytes)
    queue = deque([(H, b"")])

    while queue:
        current_H, P = queue.popleft()  # Dequeue a pair of hash function & a prefix

        if progress_callback:
            progress_callback(P, size)

        if len(P) < size:
            # Try all possible bytes in the alphabet (0-255)
            for c in range(256):
                byte_c = bytes([c])
                P_opt = P + byte_c

                H_opt = current_H.copy()
                H_opt.update(byte_c)

                # Check if the digest is in the Bloom Filter
                if H_opt.digest() in bf:
                    queue.append((H_opt, P_opt))  # Enqueue candidate pair
        else:
            # Length has reached the size, verify with postamble
            success = True
            for phi in postamble:
                byte_phi = bytes([phi])
                current_H.update(byte_phi)

                if current_H.digest() not in bf:
                    success = False
                    break  # False positive full message

            if success:
                return P

    return None
