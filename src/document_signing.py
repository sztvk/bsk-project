import os

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import unpad
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

from src.find_keys import find_private_key

RANDOM_BYTES_NUMBER = 16


def decrypt_private_key(encrypted_key_path, pin):
    """
    Decrypts a private key that has been encrypted using AES encryption with a PIN.

    This function reads the encrypted private key from the specified file, extracts the initialization vector (IV)
    and encrypted key data, and then decrypts the key using the AES algorithm. The PIN is hashed using SHA256 to
    generate the encryption key. If the decryption is successful, the private key is returned.

    If the provided PIN is incorrect, a `ValueError` is raised.

    Parameters
    ----------
    encrypted_key_path : str
        The path to the file containing the encrypted private key.
    pin : str
        The PIN used to decrypt the private key.

    Returns
    -------
    private_key : RSA key
        The decrypted private key.

    Raises
    ------
    ValueError
        If the PIN is incorrect or the decryption fails.
    """
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
    """
    Signs a PDF file using a private key stored on a USB device.

    This function first locates the encrypted private key on the USB device, decrypts it using the provided PIN,
    and then signs the specified PDF file. The signed PDF file is saved at a location chosen by the user.

    If the PDF path or the private key cannot be found, appropriate error messages are returned.

    Parameters
    ----------
    usb_path : str
        The path to the USB device where the private key is stored.
    pdf_path : str
        The path to the PDF file to be signed.
    pin : str
        The PIN used to decrypt the private key.

    Returns
    -------
    str
        A message indicating the result of the signing operation. This can be a success message or an error message.

    Raises
    ------
    FileNotFoundError
        If the encrypted private key is not found on the USB device.
    """
    encrypted_key_path = find_private_key(usb_path)

    if not pdf_path:
        return "Nie wybrano pliku."

    if not os.path.exists(encrypted_key_path):
        raise FileNotFoundError("Nie znaleziono klucza prywatnego na pendrive.")

    private_key = decrypt_private_key(encrypted_key_path, pin)

    save_file_dialog = QFileDialog()
    save_file_dialog.setDefaultSuffix('pdf')
    output_pdf_path, _ = save_file_dialog.getSaveFileName(
        None, 'Zapisz podpisany plik PDF', '', 'PDF Files (*.pdf)')

    if not output_pdf_path:
        return "Nie wybrano ścieżki zapisu."

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

    return f"Plik PDF został podpisany i zapisany jako {output_pdf_path}"
