import os

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

from src.verify_signature import verify_signature

RANDOM_BYTES_NUMBER = 16


def decrypt_private_key(encrypted_key_path, pin):
    with open(encrypted_key_path, "rb") as key_file:
        encrypted_data = key_file.read()
        iv, encrypted_key = encrypted_data[:RANDOM_BYTES_NUMBER], encrypted_data[RANDOM_BYTES_NUMBER:]

    hashed_pin = SHA256.new(pin.encode()).digest()
    cipher = AES.new(hashed_pin, AES.MODE_CBC, iv)

    try:
        private_key_pem = unpad(cipher.decrypt(encrypted_key), AES.block_size)
    except ValueError:
        raise ValueError("Niepoprawny PIN.")

    private_key = serialization.load_pem_private_key(
        private_key_pem, password=None
    )
    return private_key


def sign_pdf(usb_path, pdf_path, pin):
    encrypted_key_path = os.path.join(usb_path, "encrypted_private_key.pk")
    if not os.path.exists(encrypted_key_path):
        raise FileNotFoundError("Nie znaleziono klucza prywatnego na pendrive.")

    private_key = decrypt_private_key(encrypted_key_path, pin)
    output_pdf_path = os.path.join(usb_path, "signed_document.pdf")

    with open(pdf_path, "rb") as f:
        pdf_data = f.read()

    signature = private_key.sign(
        pdf_data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    signature_hex = signature.hex()
    byte_range = f"[0 {len(pdf_data)} {len(pdf_data)} 0]"

    sig_dict = (
        "<<\n"
        "/Type /Sig\n"
        "/Filter /Adobe.PPKLite\n"
        "/SubFilter /adbe.pkcs7.detached\n"
        f"/ByteRange {byte_range}\n"
        f"/Contents <{signature_hex}>\n"
        ">>"
    )

    new_pdf_data = pdf_data + b"\n" + sig_dict.encode('ascii')
    with open(output_pdf_path, 'wb') as f:
        f.write(new_pdf_data)

    print(f"Plik PDF został podpisany i zapisany jako {output_pdf_path}")

    return output_pdf_path


def main():
    pin = input("Podaj PIN: ")
    private_key_path = input("Podaj ścieżkę do klucza prywatnego: ")
    pendrive_path = input("Podaj ścieżkę do pendrive: ")
    pdf_path = input("Podaj ścieżkę do pliku pdf, który chcesz podpisać: ")
    public_key_path = input("Podaj ścieżkę do klucza publicznego: ")

    decrypt_private_key(private_key_path, pin)
    signed_pdf_path = sign_pdf(pendrive_path, pdf_path, pin)

    verify_signature(signed_pdf_path, public_key_path)


if __name__ == '__main__':
    main()
