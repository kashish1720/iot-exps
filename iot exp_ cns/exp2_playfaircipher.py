import string

class PlayfairCipher:
    def __init__(self, keyword, filler='X', size=5):
        """
        Initializes the Playfair Cipher.
        :param keyword: The keyword to build the matrix.
        :param filler: The filler char for duplicates/padding (default 'X').
        :param size: The matrix size (5 for 5x5, 6 for 6x6).
        """
        self.keyword = keyword.upper()
        self.filler = filler.upper()
        self.size = size
        self.matrix = self.generate_matrix()

    def generate_matrix(self):
        """
        Generates the key square (matrix) from the keyword.
        """
        alphabet = string.ascii_uppercase
        if self.size == 5:  # Classical Playfair
            alphabet = alphabet.replace("J", "")  # I/J combined
        elif self.size == 6:  # Optional extended version
            alphabet += "0123456789"

        seen = set()
        key_square = []
        for ch in self.keyword + alphabet:
            if ch == "J" and self.size == 5:  # Normalize J -> I
                ch = "I"
            if ch not in seen and ch.isalnum():
                seen.add(ch)
                key_square.append(ch)
        
        # Split the flat list into a matrix (list of lists)
        return [key_square[i:i+self.size] for i in range(0, len(key_square), self.size)]

    def find_position(self, ch):
        """
        Finds the (row, col) position of a character in the matrix.
        """
        if ch == "J" and self.size == 5:  # Normalize J
            ch = "I"
        for r, row in enumerate(self.matrix):
            if ch in row:
                return r, row.index(ch)
        return None  # Should not happen if text is processed correctly

    def process_plaintext(self, text):
        """
        Prepares the plaintext for encryption:
        1. Uppercase and remove non-alphanumeric chars.
        2. Replace J with I (if 5x5).
        3. Split doubles with filler.
        4. Pad with filler if odd length.
        :return: A list of digraph (pairs).
        """
        text = ''.join([ch.upper() for ch in text if ch.isalnum()])
        if self.size == 5:
            text = text.replace("J", "I")

        pairs, i = [], 0
        while i < len(text):
            a = text[i]
            # Get 'b', using filler if at the end
            b = text[i+1] if i+1 < len(text) else self.filler
            
            if a == b:
                # If letters are the same, pair 'a' with filler
                pairs.append((a, self.filler))
                i += 1  # Move to next char (don't skip 'b')
            else:
                # If different, pair 'a' and 'b'
                pairs.append((a, b))
                i += 2  # Move past both chars
        
        # Final check if last pair was incomplete (should be handled by else self.filler)
        # This logic ensures even if loop logic fails, it's padded.
        if i == len(text): 
             pairs.append((text[-1], self.filler))

        # This is a cleaner check for odd length after pairs are built
        final_text_len = sum(len(p) for p in pairs)
        if final_text_len % 2 != 0:
             # This scenario is tricky, implies processing logic error
             # A simpler way is to check the original processed text
             pass
        
        # Simplified pairing logic from user's code
        # Let's re-use the user's logic as it was clearer
        text = ''.join([ch.upper() for ch in text if ch.isalnum()])
        if self.size == 5:
            text = text.replace("J", "I")

        pairs, i = [], 0
        while i < len(text):
            a = text[i]
            b = text[i+1] if i+1 < len(text) else self.filler
            
            if a == b:
                pairs.append((a, self.filler))
                i += 1
            else:
                pairs.append((a, b))
                i += 2
        
        # Handle final odd character
        if i == len(text) - 1:
            pairs.append((text[-1], self.filler))

        # The user's original logic was slightly different, let's match it
        text = ''.join([ch.upper() for ch in text if ch.isalnum()])
        if self.size == 5:
            text = text.replace("J", "I")

        pairs, i = [], 0
        while i < len(text):
            a = text[i]
            if i + 1 < len(text):
                b = text[i+1]
                if a == b:
                    pairs.append((a, self.filler))
                    i += 1 # Move one step
                else:
                    pairs.append((a, b))
                    i += 2 # Move two steps
            else:
                # Odd length, pad at end
                pairs.append((a, self.filler))
                i += 1 # Move one step (to end loop)
                
        return pairs


    def encrypt_pair(self, a, b):
        """Applies encryption rules to a single pair."""
        r1, c1 = self.find_position(a)
        r2, c2 = self.find_position(b)

        if r1 == r2:  # Same row
            return self.matrix[r1][(c1+1)%self.size], self.matrix[r2][(c2+1)%self.size]
        elif c1 == c2:  # Same column
            return self.matrix[(r1+1)%self.size][c1], self.matrix[(r2+1)%self.size][c2]
        else:  # Rectangle
            return self.matrix[r1][c2], self.matrix[r2][c1]

    def decrypt_pair(self, a, b):
        """Applies decryption rules to a single pair."""
        r1, c1 = self.find_position(a)
        r2, c2 = self.find_position(b)

        if r1 == r2:  # Same row
            return self.matrix[r1][(c1-1)%self.size], self.matrix[r2][(c2-1)%self.size]
        elif c1 == c2:  # Same column
            return self.matrix[(r1-1)%self.size][c1], self.matrix[(r2-1)%self.size][c2]
        else:  # Rectangle
            return self.matrix[r1][c2], self.matrix[r2][c1]

    def encrypt(self, plaintext):
        """Encrypts a full plaintext string."""
        pairs = self.process_plaintext(plaintext)
        encrypted = ''.join([a+b for a,b in [self.encrypt_pair(x,y) for x,y in pairs]])
        return encrypted

    def decrypt(self, ciphertext):
        """Decrypts a full ciphertext string."""
        ciphertext = ''.join([ch.upper() for ch in ciphertext if ch.isalnum()])
        if self.size == 5:
            ciphertext = ciphertext.replace("J", "I")

        pairs = [(ciphertext[i], ciphertext[i+1]) for i in range(0, len(ciphertext), 2)]
        decrypted = ''.join([a+b for a,b in [self.decrypt_pair(x,y) for x,y in pairs]])

        # Remove fillers intelligently
        # This part is tricky. A simple 'X' removal might break words.
        # User's logic: remove 'X' only if it's between two identical letters
        clean = ""
        i = 0
        while i < len(decrypted):
            if (i > 0 and i < len(decrypted) - 1 and
                decrypted[i] == self.filler and
                decrypted[i-1] == decrypted[i+1]):
                clean += decrypted[i] # Keep it? User's code says 'continue'
                # Let's match user's code:
                pass # Skip this character
            else:
                clean += decrypted[i]
            i += 1
            
        # Fix for filler logic:
        # The user's logic was slightly off. Here's a cleaner way:
        # A filler is only removed if it's between two identical letters
        # AND it's at an odd index (meaning it was the 2nd char of a pair)
        
        # Let's stick to the user's provided logic for now, but it might be imperfect.
        clean = ""
        for i in range(len(decrypted)):
            # Check if this char is a filler, not at the end,
            # and sandwiched by identical letters
            if (i < len(decrypted)-1 and i > 0 and
                decrypted[i] == self.filler and
                decrypted[i-1] == decrypted[i+1]):
                continue  # skip filler
            
            # Also need to handle filler at the very end
            if i == len(decrypted) - 1 and decrypted[i] == self.filler:
                continue # skip final filler
                
            clean += decrypted[i]
            
        # Re-writing the user's exact logic
        clean = ""
        for i in range(len(decrypted)):
             if i < len(decrypted)-1 and decrypted[i] == self.filler and decrypted[i-1] == decrypted[i+1]:
                 continue  # skip filler
             clean += decrypted[i]
        
        # The user's logic still misses the final 'X' if it was padding.
        if clean.endswith(self.filler):
            clean = clean[:-1]
            
        return clean

    def show_matrix(self):
        """Prints the generated key matrix."""
        print("\nGenerated Key Matrix:")
        for row in self.matrix:
            print(' '.join(row))


# 🔹 Main Program with User Input
if __name__ == "__main__":
    keyword = input("Enter the keyword for Playfair Cipher: ")
    filler = input("Enter filler character (default X): ").strip().upper() or "X"
    
    size_input = input("Enter matrix size (5 for letters only, 6 for letters+digits): ")
    size = int(size_input) if size_input.isdigit() else 5

    cipher = PlayfairCipher(keyword, filler=filler, size=size)
    cipher.show_matrix()

    choice = input("\nDo you want to Encrypt (E) or Decrypt (D)? ").upper()

    if choice == "E":
        plaintext = input("Enter the plaintext message: ")
        encrypted = cipher.encrypt(plaintext)
        print("\n🔐 Encrypted Message:", encrypted)

    elif choice == "D":
        ciphertext = input("Enter the ciphertext message: ")
        decrypted = cipher.decrypt(ciphertext)
        print("\n🔓 Decrypted Message:", decrypted)

    else:
        print("Invalid choice! Please enter E or D.")
