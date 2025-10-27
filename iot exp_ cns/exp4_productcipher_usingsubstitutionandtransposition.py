# Product Cipher with Substitution + Transposition
# Takes user input and supports bigger matrix

def substitution_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            result += chr((ord(char) - ord(base) + shift) % 26 + ord(base))
        else:
            result += char
    return result

def substitution_decrypt(text, shift):
    return substitution_encrypt(text, -shift)

def transposition_encrypt(text, key):
    # Make matrix row-wise
    matrix = [list(text[i:i+key]) for i in range(0, len(text), key)]

    # Padding with underscores if last row is short
    if len(matrix[-1]) < key:
        matrix[-1] += ['_'] * (key - len(matrix[-1]))

    print("\nMatrix during Encryption:")
    for row in matrix:
        print(" ".join(row))

    # Read column-wise
    ciphertext = ""
    for col in range(key):
        for row in matrix:
            ciphertext += row[col]
    return ciphertext

def transposition_decrypt(ciphertext, key):
    n = len(ciphertext)
    rows = (n + key - 1) // key
    extra = n % key if n % key != 0 else key
    col_lengths = [rows if i < extra else rows-1 for i in range(key)]

    # Prepare empty matrix
    matrix = [[""] * key for _ in range(rows)]
    index = 0
    for col in range(key):
        for row in range(col_lengths[col]):
            matrix[row][col] = ciphertext[index]
            index += 1

    print("\nMatrix during Decryption:")
    for row in matrix:
        print(" ".join(ch if ch else "_" for ch in row))

    # Read row-wise
    plaintext = ""
    for row in matrix:
        plaintext += "".join(row)
    return plaintext.replace("_", "")

def product_encrypt(plaintext, shift, key):
    step1 = substitution_encrypt(plaintext, shift)
    print("\nAfter Substitution:", step1)
    step2 = transposition_encrypt(step1, key)
    return step2

def product_decrypt(ciphertext, shift, key):
    step1 = transposition_decrypt(ciphertext, key)
    print("\nAfter Reverse Transposition:", step1)
    step2 = substitution_decrypt(step1, shift)
    return step2

# --- User Input ---
plaintext = input("Enter Plaintext: ").upper()
shift = int(input("Enter Substitution Shift Key (e.g., 3): "))
key = int(input("Enter Transposition Key (matrix column size, e.g., 4): "))

print("\n=== Encryption ===")
ciphertext = product_encrypt(plaintext, shift, key)
print("Ciphertext:", ciphertext)

print("\n=== Decryption ===")
decrypted = product_decrypt(ciphertext, shift, key)
print("Decrypted Text:", decrypted)

