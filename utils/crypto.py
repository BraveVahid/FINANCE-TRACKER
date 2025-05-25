class CryptoManager:
    a, b = 17, 21
    str_key = 1

    @classmethod
    def encrypt_number(cls, number):
        try:
            a, b = cls.a , cls.b
            number = float(number)
            encrypted_number = a * number + b
            return encrypted_number
        except ValueError:
            return None

    @classmethod
    def decrypt_number(cls, encrypted_number):
        try:
            encrypted_number = float(encrypted_number)
            a, b = cls.a, cls.b
            decrypted_number = (encrypted_number - b) / a
            return decrypted_number
        except ValueError:
            return None

    @classmethod
    def encrypt_string(cls, plain_text):
        try:
            encrypted = ""
            for char in plain_text.lower():
                encrypted += chr((ord(char) + cls.str_key))
            return encrypted
        except:
            return None

    @classmethod
    def decrypt_string(cls, encrypted_text):
        try:
            decrypted = ""
            for char in encrypted_text.lower():
                decrypted += chr((ord(char) - cls.str_key))
            return decrypted
        except:
            return None
