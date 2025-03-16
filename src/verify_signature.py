import re

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization


def verify_signature(pdf_path, public_key_path):
    with open(public_key_path, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())

    with open(pdf_path, 'rb') as f:
        full_pdf = f.read()

    sig_dict_start = full_pdf.rfind(b'<<\n/Type /Sig')
    sig_dict_end = full_pdf.rfind(b'>\n>>') + 4
    if sig_dict_start == -1:
        return "Brak podpisu w pliku PDF."

    sig_dict_data = full_pdf[sig_dict_start:]

    contents_match = re.search(rb'/Contents\s*<([0-9A-Fa-f]+)>', sig_dict_data)
    if not contents_match:
        return "Nie znaleziono pola /Contents w słowniku podpisu."

    signature_hex = contents_match.group(1)
    try:
        signature = bytes.fromhex(signature_hex.decode('ascii'))
    except Exception as e:
        return "Błąd przy konwersji podpisu z hex"

    data_to_verify = full_pdf[:sig_dict_start].rstrip() + full_pdf[sig_dict_end:].rstrip() + b"\n"

    try:
        public_key.verify(
            signature,
            data_to_verify,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return "Podpis jest ważny!"
    except Exception as e:
        return "Plik został zmodyfikowany. Podpis jest nieważny!"