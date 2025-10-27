import random
from math import gcd

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_prime_candidate(start=100, end=300):
    while True:
        p = random.randint(start, end)
        if is_prime(p):
            return p

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

    return (e, n), (d, n)

def encrypt(plaintext, public_key):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(ciphertext, private_key):
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

def main():
    print("RSA Cryptosystem Implementation")
    public_key, private_key = generate_keys()
    print(f"Generated Public Key (e, n): {public_key}")
    print(f"Generated Private Key (d, n): {private_key}")

    message = input("Enter the message to encrypt: ")
    encrypted_msg = encrypt(message, public_key)
    print(f"Encrypted Message (numeric): {encrypted_msg}")

    decrypted_msg = decrypt(encrypted_msg, private_key)
    print(f"Decrypted Message: {decrypted_msg}")

if __name__ == "__main__":
    main()
