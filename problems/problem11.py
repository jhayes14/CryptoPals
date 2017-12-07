from cryptofuncs import *


if __name__ == "__main__":

    cipher_texts = []
    plain_text = 'A' * 200
    for i in xrange(10):
        cipher, mode = encryption_oracle(plain_text, debug=False)
        cipher_texts.append((cipher, mode))
    cipher_texts = [(x[0], x[1]) for x in cipher_texts]
    for cipher, mode in cipher_texts:
        if detect_ECB(cipher):
            print "True mode: %s Predicted mode: %s" %(mode, "ECB")
        else:
            print "True mode: %s Predicted mode: %s" %(mode, "CBC")
