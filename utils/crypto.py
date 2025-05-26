class CryptoManager:
    a, b = 17, 21
    str_key = 1

    @classmethod
    def encrypt_number(cls, number):
        a, b = cls.a , cls.b
        encrypted_number = a * number + b
        return encrypted_number

    @classmethod
    def decrypt_number(cls, encrypted_number):
        a, b = cls.a, cls.b
        decrypted_number = (encrypted_number - b) / a
        return decrypted_number

    @classmethod
    def encrypt_string(cls, plain_text):
        encrypted = ""
        for char in plain_text:
            encrypted += chr((ord(char) + cls.str_key))
        return encrypted

    @classmethod
    def decrypt_string(cls, encrypted_text):
        decrypted = ""
        for char in encrypted_text:
            decrypted += chr((ord(char) - cls.str_key))
        return decrypted
