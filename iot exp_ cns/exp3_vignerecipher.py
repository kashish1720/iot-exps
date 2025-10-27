def clean(text):
    """
    Cleans the text by removing non-alphabetic characters
    and converting to uppercase.
    """
    # Use a generator expression for efficiency
    return "".join(c for c in text if c.isalpha()).upper()

def encrypt(plaintext, key):
    """
    Encrypts the plaintext using the Vigenere cipher.
    Formula: C = (P + K) % 26
    """
    plaintext = clean(plaintext)
    key = clean(key)
    cipher = []
    
    # Check for empty key to avoid ZeroDivisionError
    if not key:
        print("Error: Key cannot be empty.")
        return plaintext
        
    for i in range(len(plaintext)):
        # Get numeric value (A=0, B=1, ...)
        p = ord(plaintext[i]) - ord('A')
        k = ord(key[i % len(key)]) - ord('A')
        
        # Apply formula
        c = (p + k) % 26
        
        # Convert back to character
        cipher.append(chr(c + ord('A')))
        
    return "".join(cipher)

def decrypt(ciphertext, key):
    """
    Decrypts the ciphertext using the Vigenere cipher.
    Formula: P = (C - K + 26) % 26
    """
    ciphertext = clean(ciphertext)
    key = clean(key)
    plain = []
    
    # Check for empty key to avoid ZeroDivisionError
    if not key:
        print("Error: Key cannot be empty.")
        return ciphertext
        
    for i in range(len(ciphertext)):
        # Get numeric value (A=0, B=1, ...)
        c = ord(ciphertext[i]) - ord('A')
        k = ord(key[i % len(key)]) - ord('A')
        
        # Apply formula
        # We add 26 to handle negative numbers (e.g., C=0, K=1 -> -1)
        p = (c - k + 26) % 26
        
        # Convert back to character
        plain.append(chr(p + ord('A')))
        
    return "".join(plain)

# The `if __name__ == "__main__":` block ensures this code
# only runs when the script is executed directly.
if __name__ == "__main__":
    """
    Main function to get user input and run the program.
    """
    try:
        text = input("Enter text (Plaintext or Ciphertext): ")
        key = input("Enter key: ")
        
        # Get choice, make it uppercase, and remove whitespace
        choice = input("Choose operation (E for Encrypt, D for Decrypt): ").upper().strip()

        if not key.isalpha():
            print("\nWarning: Key should only contain alphabetic characters for a standard Vigenere cipher.")
            key = clean(key) # Clean the key to be safe
            print(f"Using cleaned key: {key}")

        if not key:
             print("\nError: A valid key is required to encrypt or decrypt.")
        elif choice.startswith('E'):
            cipher = encrypt(text, key)
            print(f"\n🔐 Encrypted Text: {cipher}")
        elif choice.startswith('D'):
            plain = decrypt(text, key)
            print(f"\n🔓 Decrypted Text: {plain}")
        else:
            print("\nInvalid choice! Please enter E or D.")
            
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

