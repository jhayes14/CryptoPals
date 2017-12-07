from cryptofuncs import *
import re

def CBC_oracle(plaintext, key, IV):
    prepend = "comment1=cooking%20MCs;userdata="
    append = ";comment2=%20like%20a%20pound%20of%20bacon"
    plaintext = prepend + plaintext + append
    plaintext = plaintext.replace(";", "").replace("=", "")
    padplaintext = pkcs7_pad_alt(plaintext, 16)
    return encrypt_AES_CBC(padplaintext, key, IV)


def is_admin(ciphertext, key, IV):
    plaintext = decrypt_AES_CBC(ciphertext, key, IV)
    result = re.search(b';admin=true;', plaintext)
    return bool(result)

def flip_bits(ciphertext):
    ciphertext_array = bytearray(ciphertext)
    byte_x = ciphertext_array[34]
    ciphertext_array[34] = byte_x ^ 1
    byte_y = ciphertext_array[40]
    ciphertext_array[40] = byte_y ^ 125
    byte_z = ciphertext_array[45]
    ciphertext_array[45] = byte_z ^ 88
    return str(ciphertext_array)

if __name__ == '__main__':

    key = generate_AES_key()
    IV = generate_AES_key()
    attack_text = "A"*16 + "AAAAA:admin@true"
    original_ciphertext = CBC_oracle(attack_text, key, IV)
    attack_ciphertext = flip_bits(original_ciphertext)
    print "';admin=true;' found?", is_admin(attack_ciphertext, key, IV)
