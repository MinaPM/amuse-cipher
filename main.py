import sys
import hashlib
import time
import pickle
from algo1 import encrypt_file
from algo2 import decrypt_file


def render_progress(current_prefix: bytes, total_size: int):
    """Callback to visualize decryption progress."""
    # Safely convert the prefix to string for visualization
    decoded = repr(current_prefix)
    if len(decoded) > 20:
        decoded = "..." + decoded[-17:]

    # Calculate progress for the bar
    progress = len(current_prefix) / total_size if total_size > 0 else 1.0
    bar_length = 30
    filled = int(bar_length * progress)
    bar = "=" * filled + "-" * (bar_length - filled)

    # Use color in output
    c_blue = "\033[94m"
    c_green = "\033[92m"
    c_yellow = "\033[93m"
    c_reset = "\033[0m"

    # \r returns carriage to start of line to overwrite
    # \033[K clears the rest of the line to prevent leftover characters
    sys.stdout.write(
        f"\r{c_blue}Decryption:{c_reset} [{c_green}{bar}{c_reset}] {len(current_prefix)}/{total_size} bytes | {c_yellow}Guessing: '{decoded}'{c_reset}\033[K"
    )
    sys.stdout.flush()


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    try:
        with open(input_file, "rb") as f:
            message = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    # 1. Setup our testing parameters
    postamble = b"END"
    prob = 0.001  # False positive probability

    print("=== AMUSE Cipher Proof of Concept ===")
    print(f"Input File:       {input_file}")
    print(f"File Size:        {len(message)} bytes")
    print(f"Postamble:        {postamble}")
    print(f"Target FPR:       {prob}")
    print("-" * 50)

    # 2. Encrypt the message
    start_time = time.time()
    # We use hashlib.sha256() as our hash function H
    bf = encrypt_file(message, hashlib.sha256(), prob, postamble)
    encrypt_time = time.time() - start_time

    print(f"Encryption Time:  {encrypt_time:.4f} seconds")
    print(f"Bloom Filter Capacity: {bf.num_bits_m} bits")

    encrypted_file = input_file + ".enc"
    with open(encrypted_file, "wb") as f:
        pickle.dump({
            "bf": bf,
            "size": len(message),
            "postamble": postamble
        }, f)
    print(f"Encrypted data saved to: {encrypted_file}")

    # 3. Decrypt the message
    start_time = time.time()

    # Load the encrypted data
    with open(encrypted_file, "rb") as f:
        loaded_data = pickle.load(f)

    loaded_bf = loaded_data["bf"]
    loaded_size = loaded_data["size"]
    loaded_postamble = loaded_data["postamble"]

    # Note: We must supply a fresh hash object for decryption
    # and we pass our render_progress callback
    decrypted_message = decrypt_file(
        loaded_bf, hashlib.sha256(), loaded_size, loaded_postamble, progress_callback=render_progress
    )
    decrypt_time = time.time() - start_time

    print()  # Add a newline after the progress bar finishes
    print(f"Decryption Time:  {decrypt_time:.4f} seconds")
    print("-" * 50)

    # 4. Verify results
    if decrypted_message is not None and decrypted_message == message:
        print("[SUCCESS] Decrypted message matches original!")
        output_file = input_file + ".decrypted"
        with open(output_file, "wb") as f:
            f.write(decrypted_message)
        print(f"Decrypted output saved to: {output_file}")
    else:
        print("[FAILED] Decrypted message does NOT match original.")


if __name__ == "__main__":
    main()
