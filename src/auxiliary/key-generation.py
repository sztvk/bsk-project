import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

RSA_KEY_SIZE = 4096
PUBLIC_EXPONENT = 65537


def get_user_pin():
    user_pin = input("Enter your PIN: ")

    return user_pin


def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=PUBLIC_EXPONENT, key_size=RSA_KEY_SIZE,
                                           backend=default_backend())
    public_key = private_key.public_key()

    return private_key, public_key


def encrypt_private_key(private_key, pin):
    iv = os.urandom(16)

    hashed_pin = SHA256.new(pin.encode()).digest()
    cipher = AES.new(hashed_pin, AES.MODE_CBC, iv)

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    encrypted_key = cipher.encrypt(pad(private_key_bytes, AES.block_size))

    return iv + encrypted_key


def get_directory_to_save_keys():
    directory = input("Enter the directory where you want to save the keys: ")

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def save_keys(public_key, private_key, directory):
    public_key_path = os.path.join(directory, "public_key.pubk")
    with open(public_key_path, "wb") as public_key_file:
        public_key_file.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    private_key_path = os.path.join(directory, "encrypted_private_key.pk")
    with open(private_key_path, "wb") as private_key_file:
        private_key_file.write(private_key)


def main():
    pin = get_user_pin()
    private_key, public_key = generate_keys()
    private_key_encrypted = encrypt_private_key(private_key, pin)
    directory = get_directory_to_save_keys()
    save_keys(public_key, private_key_encrypted, directory)


if __name__ == '__main__':
    main()
