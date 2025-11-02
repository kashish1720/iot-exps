import random
from math import gcd

# Check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Generate a random prime number between given range
def generate_prime_candidate(start=100, end=300):
    while True:
        p = random.randint(start, end)
        if is_prime(p):
            return p

# Calculate modular inverse using Extended Euclidean Algorithm
def mod_inverse(e, phi):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)
    g, x, _ = egcd(e, phi)
    if g != 1:
        return None
    else:
        return x % phi

# Generate RSA keys (public and private) along with primes p and q
def generate_keys():
    p = generate_prime_candidate()
    q = generate_prime_candidate()
    while q == p:
        q = generate_prime_candidate()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = mod_inverse(e, phi)

    return (e, n), (d, n), p, q

# Encrypt text message
def encrypt_text(plaintext, public_key):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

# Decrypt text message
def decrypt_text(ciphertext, private_key):
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

# Encrypt numeric message
def encrypt_number(number, public_key):
    e, n = public_key
    return pow(number, e, n)

# Decrypt numeric message
def decrypt_number(cipher_num, private_key):
    d, n = private_key
    return pow(cipher_num, d, n)

# Main function
def main():
    print("===== RSA Cryptosystem Implementation =====")

    # Generate keys
    public_key, private_key, p, q = generate_keys()

    print(f"\nPrime numbers (p, q): {p}, {q}")
    print(f"Public Key (e, n): {public_key}")
    print(f"Private Key (d, n): {private_key}")

    # --- Text Message Encryption ---
    message = input("\nEnter a TEXT message to encrypt: ")
    encrypted_text = encrypt_text(message, public_key)
    print(f"Encrypted Text Message (numeric list): {encrypted_text}")

    decrypted_text = decrypt_text(encrypted_text, private_key)
    print(f"Decrypted Text Message: {decrypted_text}")

    # --- Numeric Message Encryption ---
    try:
        num_message = int(input("\nEnter a NUMERIC message to encrypt (less than n): "))
        if num_message >= public_key[1]:
            print("Error: Message must be less than n!")
        else:
            encrypted_num = encrypt_number(num_message, public_key)
            print(f"Encrypted Numeric Message: {encrypted_num}")

            decrypted_num = decrypt_number(encrypted_num, private_key)
            print(f"Decrypted Numeric Message: {decrypted_num}")
    except ValueError:
        print("Invalid numeric input!")

# Run the program
if __name__ == "__main__":
    main()
