import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad

RSA_KEY_SIZE = 4096
PUBLIC_EXPONENT = 65537


def generate_keys():
    """
    Generates a pair of RSA keys: a private key and a public key.

    This function uses the cryptography library to generate an RSA private key with the specified key size and public exponent.
    The corresponding public key is derived from the private key.

    Returns
    -------
    private_key : RSA key
        The generated private key.
    public_key : RSA key
        The generated public key.
    """
    private_key = rsa.generate_private_key(public_exponent=PUBLIC_EXPONENT, key_size=RSA_KEY_SIZE,
                                           backend=default_backend())
    public_key = private_key.public_key()

    return private_key, public_key


def encrypt_private_key(private_key, pin):
    """
    Encrypts the private key using AES encryption with a key derived from the provided PIN.

    This function uses AES encryption in CBC mode to encrypt the private key. The PIN is hashed using SHA-256
    and then used as the key for the AES encryption. A random initialization vector (IV) is generated for the CBC mode.

    Parameters
    ----------
    private_key : RSA key
        The private key to be encrypted.
    pin : str
        The PIN used to generate the encryption key.

    Returns
    -------
    encrypted_key : bytes
        The encrypted private key, which includes the IV followed by the encrypted data.
    """
    iv = os.urandom(16)

    # Hash the PIN to create a key for AES encryption
    hashed_pin = SHA256.new(pin.encode()).digest()
    cipher = AES.new(hashed_pin, AES.MODE_CBC, iv)

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    encrypted_key = cipher.encrypt(pad(private_key_bytes, AES.block_size))

    return iv + encrypted_key


def save_keys(public_key, private_key, directory, directory_pub):
    """
    Saves the public and encrypted private keys to the specified directory.

    This function writes the public key to a `.pubk` file and the encrypted private key to a `.pk` file.
    Both files are saved in the specified directory.

    Parameters
    ----------
    public_key : RSA key
        The public key to be saved.
    private_key : bytes
        The encrypted private key to be saved.
    directory : str
        The directory where the keys will be saved.
    """
    public_key_path = os.path.join(directory_pub, "public_key.pubk")
    with open(public_key_path, "wb") as public_key_file:
        public_key_file.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    private_key_path = os.path.join(directory, "encrypted_private_key.pk")
    with open(private_key_path, "wb") as private_key_file:
        private_key_file.write(private_key)


def key_generator(pin, directory, directory_pub):
    """
    Generates a pair of RSA keys, encrypts the private key using the provided PIN, and saves the keys to a directory.

    This function calls `generate_keys` to generate the keys, then `encrypt_private_key` to encrypt the private key,
    and finally `save_keys` to save the keys to disk.

    Parameters
    ----------
    pin : str
        The PIN used to encrypt the private key.
    directory : str
        The directory where the keys will be saved.

    Returns
    -------
    None
    """
    private_key, public_key = generate_keys()
    private_key_encrypted = encrypt_private_key(private_key, pin)
    save_keys(public_key, private_key_encrypted, directory, directory_pub)
