# PAdES Qualified Electronic Signature System
Project carried out as part of the course in Computer Systems Security (Bezpieczeństwo Systemów Komputerowych) at the Gdansk University of Technology.
## Project Description
This project implements a qualified PAdES electronic signature process for PDF files. It consists of two applications:

1. **Auxiliary Application** - Generates an RSA key pair, encrypts the private key using AES-256, and stores it on a selected USB device. The public key can be saved in any chosen directory.
2. **Main Application** - Allows users to sign PDF documents and verify their authenticity.

### Features:
- Generation and encryption of RSA keys.
- Detection of USB devices for key storage.
- Signing and verification of PDF files in compliance with the PAdES standard.
- Automatic key detection.
- Intuitive user interface.

## Installation
The project requires Python 3.8+.

### Creating a Virtual Environment
To avoid dependency conflicts, it is recommended to use a virtual environment:
```sh
python -m venv venv
```
### Activating the Virtual Environment
*Windows:*
```sh
venv\Scripts\activate
```
*MacOS/Linux:*
```sh
source venv/bin/activate
```
### Installing Dependencies
This project requires the following Python libraries:
- pycryptodome
- cryptography
- PyQt6
    
```sh
pip install -r requirements.txt
```
### Running the Application
*Auxiliary Application (Key Generation):*
```sh
python auxiliary_app.py
```
*Main Application (Signing and Verifying Documents)*
```sh
python main_app.py
```
### Authors
- Anna Sztukowska
- Martyna Koźbiał
