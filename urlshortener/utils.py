import hashlib

enc_table_64 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"

def int_to_enc(n, enc_table):
    base = len(enc_table)
    digits = ""
    while n:
        digits += enc_table[int(n % base)]
        n //= base
    return digits[::-1]

def shortcode(url, char_length=8, enc_table=enc_table_64):
    hash_object = hashlib.sha512(url.encode())
    hash_hex = hash_object.hexdigest()
    hash_enc = int_to_enc(int(hash_hex, 16), enc_table)
    return hash_enc[0:char_length]