from cryptofuncs import *


if __name__ == "__main__":
    #print parser("foo=bar&baz=qux&zap=zazzle")
    encode_profile = profile_for("foo@bar.com=&role")
    key = generate_AES_key()
    encrypted_profile = ECB_encrypt(encode_profile, key)
    decrypted_profile = ECB_decrypt(encrypted_profile, key )
    print decrypted_profile


    # Challenge: Make a role=admin profile using only profile_for to generate ciphertexts and the ciphertexts
    base_email = "foo_1@bar.com"
    base_profile = profile_for(base_email)
    encr_base_prof = ECB_encrypt(base_profile, key)

    attack_email = ' ' * 10 + 'admin'
    attack_profile = profile_for(attack_email)
    encr_attack_prof =  ECB_encrypt(attack_profile, key)

    print ECB_decrypt(encr_base_prof[:32], key)
    print ECB_decrypt(encr_attack_prof[16:32], key)
    chosen_profile = ECB_decrypt(encr_base_prof[:32] + encr_attack_prof[16:32], key)
    print chosen_profile
