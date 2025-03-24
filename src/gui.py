import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QListWidget, QMessageBox, QTextEdit, QInputDialog, QCheckBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from src.detecting_usb import detect_usb_devices
from src.document_signing import sign_pdf
from src.find_keys import find_public_key
from src.verify_signature import verify_signature


def select_folder_pub_key(status_label, window):
    """
    Selects a folder for storing the public key.

    Opens a file dialog allowing the user to select a directory to save the public key.
    Updates the UI labels accordingly.

    If the USB device for the private key has not been selected, the user is prompted to do so.

    Parameters
    ----------
    status_label : QLabel
        The label in the user interface that provides status updates and prompts the user for further actions.
    window : QWidget
        The main application window used for displaying and interacting with the user interface.

    Returns
    -------
    selected_folder_pub_key : str
        The path of the folder selected for storing the public key.
    """
    selected_folder_pub_key = QFileDialog.getExistingDirectory(window, 'Wybierz folder z kluczem publicznym')
    status_label.setText(f"Wybrano folder z kluczem publicznym: {selected_folder_pub_key}")
    status_label.setStyleSheet("""
                    font-family: 'Verdana', sans-serif;
                    font-size: 14px;
                    color: #006600;
                    padding: 5px;
                    border-radius: 5px;
                    background-color: #E6FFE6;
                    margin-top: 10px;
                    font-weight: normal;
                """)
    return selected_folder_pub_key


def select_file(window, file_preview, status_label, button_sign_document, button_verify_signature, pub_key_button, checkbox_same_folder):
    """
    Opens a dialog to select a PDF file and displays its path in the widget.

    This function allows the user to choose a PDF file, and then updates the file preview widget and the status in the GUI.
    Once both a file and a USB drive are selected, the user can sign or verify the document.

    Parameters
    ----------
    window : QWidget
        The main application window used for displaying and interacting with the user interface.
    file_preview : QLabel
        The label in the user interface that displays the path of the selected PDF file.
    status_label : QLabel
        The label in the user interface that provides status updates and prompts the user for further actions.
    button_sign_document : QPushButton
        The button that allows the user to sign the PDF document once both the file and USB drive are selected.
    button_verify_signature : QPushButton
        The button that allows the user to verify the signature of the PDF document once both the file and USB drive are selected.
    pub_key_button : QPushButton
        The button to select the public key folder for document signature or verification.
    checkbox_same_folder : QCheckBox
        The checkbox that determines if the private and public key should be stored in the same folder.

    Returns
    -------
    None.
    """
    file_dialog = QFileDialog()
    file_path, _ = file_dialog.getOpenFileName(window, 'Wybierz plik PDF', '', 'PDF Files (*.pdf)')
    if file_path:
        file_path = file_path.replace("/", "\\")
        window.selected_file = file_path
        file_preview.setText(f'📜 Wybrany plik: {file_path}')

        if window.selected_file and window.selected_pendrive:
            status_label.setText("Plik PDF i nośnik USB wybrane. Możesz podpisać lub zweryfikować dokument.")
            status_label.setStyleSheet("""
                font-family: 'Verdana', sans-serif;
                font-size: 14px;
                color: #006600;
                padding: 5px;
                border-radius: 5px;
                background-color: #E6FFE6;
                margin-top: 10px;
                font-weight: normal;
            """)
            button_sign_document.setVisible(True)
            button_verify_signature.setVisible(True)
            pub_key_button.setVisible(True)
            checkbox_same_folder.setVisible(True)
        else:
            status_label.setText("Plik PDF wybrany. Wybierz nośnik USB.")
            status_label.setStyleSheet("""
                font-family: 'Verdana', sans-serif;
                font-size: 14px;
                color: #0066CC;
                padding: 5px;
                border-radius: 5px;
                background-color: #E6F2FF;
                margin-top: 10px;
                font-weight: normal;
            """)
            button_sign_document.setVisible(False)
            button_verify_signature.setVisible(False)
            pub_key_button.setVisible(False)
            checkbox_same_folder.setVisible(False)


def refresh_usb(status_label, app, usb_list, window, button_sign_document, button_verify_signature, pub_key_button, checkbox_same_folder):
    """
    Refreshes the list of detected USB devices.

    This function searches for connected USB devices and updates the list in the user interface. It provides status updates
    to the user, indicating whether devices were detected or if no devices were found. If devices are detected, the user
    can select one from the list, which will then enable the functionality to sign or verify the document.

    Parameters
    ----------
    status_label : QLabel
        The label in the user interface that provides status updates and prompts the user for further actions.
    app : QApplication
        The main application instance responsible for managing the application's event loop and updating the interface.
    usb_list : QListWidget
        The list widget that displays the detected USB devices for the user to select.
    window : QWidget
        The main application window used for displaying and interacting with the user interface.
    button_sign_document : QPushButton
        The button that allows the user to sign the document, visible once a USB device is selected.
    button_verify_signature : QPushButton
        The button that allows the user to verify the signature on the document, visible once a USB device is selected.
    pub_key_button : QPushButton
        The button that allows the user to select the folder for the public key, visible once a USB device is selected.
    checkbox_same_folder : QCheckBox
        The checkbox that allows the user to decide if both private and public keys should be stored in the same folder.

    Returns
    -------
    None.
    """

    status_label.setText("Wyszukiwanie nośników USB...")
    status_label.setStyleSheet("""
        font-family: 'Verdana', sans-serif;
        font-size: 14px;
        color: #FF6600;
        padding: 5px;
        border-radius: 5px;
        background-color: #FFF3E6;
        margin-top: 10px;
        font-weight: normal;
    """)
    app.processEvents()

    usb_list.clear()
    devices = detect_usb_devices()
    usb_list.addItems([f"{dev}" for dev in devices])

    if devices:
        status_label.setText(f"Liczba wykrytych nośników USB: {len(devices)}. Wybierz jeden z listy.")
        status_label.setStyleSheet("""
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #0066CC;
            padding: 5px;
            border-radius: 5px;
            background-color: #E6F2FF;
            margin-top: 10px;
            font-weight: normal;
        """)
    else:
        status_label.setText("Nie wykryto żadnych nośników USB. Podłącz nośnik i odśwież listę.")
        status_label.setStyleSheet("""
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #CC0000;
            padding: 5px;
            border-radius: 5px;
            background-color: #FFEEEE;
            margin-top: 10px;
            font-weight: normal;
        """)
    window.selected_pendrive = None
    button_sign_document.setVisible(False)
    button_verify_signature.setVisible(False)
    pub_key_button.setVisible(False)
    checkbox_same_folder.setVisible(False)

def select_usb_device(window, usb_list, button_sign_document, button_verify_signature, pub_key_button, checkbox_same_folder, status_label):
    """
    Handles the selection of a USB device from the list.

    This function sets the selected USB device and updates the interface widgets, including enabling the buttons for
    signing and verifying the document. The status is also updated based on the selection.

    Parameters
    ----------
    window : QWidget
        The main application window used for displaying and interacting with the user interface.
    usb_list : QListWidget
        The list widget containing the available USB devices, from which the user selects one.
    button_sign_document : QPushButton
        The button that allows the user to sign the document, visible once both a PDF file and USB device are selected.
    button_verify_signature : QPushButton
        The button that allows the user to verify the document's signature, visible once both a PDF file and USB device are selected.
    pub_key_button : QPushButton
        The button that allows the user to select the public key folder, visible once both a PDF file and USB device are selected.
    checkbox_same_folder : QCheckBox
        The checkbox that allows the user to specify whether to store both the private and public keys in the same folder.
    status_label : QLabel
        The label in the user interface that provides status updates and prompts the user for further actions.

    Returns
    -------
    None.
    """
    window.selected_pendrive = usb_list.currentItem().text()

    if window.selected_file and window.selected_pendrive:
        button_sign_document.setVisible(True)
        button_verify_signature.setVisible(True)
        pub_key_button.setVisible(True)
        checkbox_same_folder.setVisible(True)
        status_label.setText("Plik PDF i nośnik USB wybrane. Możesz podpisać lub zweryfikować dokument.")
        status_label.setStyleSheet("""
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #006600;
            padding: 5px;
            border-radius: 5px;
            background-color: #E6FFE6;
            margin-top: 10px;
            font-weight: normal;
        """)
    else:
        button_sign_document.setVisible(False)
        button_verify_signature.setVisible(False)
        pub_key_button.setVisible(False)
        checkbox_same_folder.setVisible(False)

        if window.selected_pendrive:
            status_label.setText("Nośnik USB wybrany. Wybierz plik PDF.")
            status_label.setStyleSheet("""
                font-family: 'Verdana', sans-serif;
                font-size: 14px;
                color: #0066CC;
                padding: 5px;
                border-radius: 5px;
                background-color: #E6F2FF;
                margin-top: 10px;
                font-weight: normal;
            """)
        else:
            status_label.setText("Wybierz plik PDF i nośnik USB.")
            status_label.setStyleSheet("""
                font-family: 'Verdana', sans-serif;
                font-size: 14px;
                color: #0066CC;
                padding: 5px;
                border-radius: 5px;
                background-color: #E6F2FF;
                margin-top: 10px;
                font-weight: normal;
            """)


def sign_document(window, status_label, app):
    """
    Handles the document signing process.

    This function opens a dialog to input the PIN, then processes the selected PDF file using the private key from the
    selected USB device. The user interface status is updated during the signing process.

    Parameters
    ----------
    window : QWidget
        The main application window used for displaying and interacting with the user interface.
    status_label : QLabel
        The label in the user interface that provides status updates and prompts the user for further actions.
    app : QApplication
        The main application instance responsible for managing the application's event loop and updating the interface.

    Returns
    -------
    None.
    """
    pin, ok = QInputDialog.getText(window, 'Wprowadź PIN', 'Podaj PIN do klucza:')

    if ok and pin:
        try:
            status_label.setText("Podpisywanie dokumentu...")
            status_label.setStyleSheet("""
                font-family: 'Verdana', sans-serif;
                font-size: 14px;
                color: #FF6600;
                padding: 5px;
                border-radius: 5px;
                background-color: #FFF3E6;
                margin-top: 10px;
                font-weight: normal;
            """)
            app.processEvents()

            pin = str(pin)
            mess = sign_pdf(window.selected_pendrive, window.selected_file, pin)

            status_label.setText(mess)
            status_label.setStyleSheet("""
                font-family: 'Verdana', sans-serif;
                font-size: 14px;
                color: #006600;
                padding: 5px;
                border-radius: 5px;
                background-color: #E6FFE6;
                margin-top: 10px;
                font-weight: normal;
            """)
        except ValueError:
            status_label.setText("Błąd! Nieprawidłowy PIN.")
            status_label.setStyleSheet("""
                font-family: 'Verdana', sans-serif;
                font-size: 14px;
                color: #CC0000;
                padding: 5px;
                border-radius: 5px;
                background-color: #FFEEEE;
                margin-top: 10px;
                font-weight: normal;
            """)
        except Exception as e:
            status_label.setText(f"Błąd podczas podpisywania: {str(e)}")
            status_label.setStyleSheet("""
                font-family: 'Verdana', sans-serif;
                font-size: 14px;
                color: #CC0000;
                padding: 5px;
                border-radius: 5px;
                background-color: #FFEEEE;
                margin-top: 10px;
                font-weight: normal;
            """)
    else:
        status_label.setText("Błąd! PIN nie został wprowadzony.")
        status_label.setStyleSheet("""
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #CC0000;
            padding: 5px;
            border-radius: 5px;
            background-color: #FFEEEE;
            margin-top: 10px;
            font-weight: normal;
        """)
        QMessageBox.warning(window, 'Błąd', 'PIN nie został wprowadzony.')


def signature_verification(status_label, app, checkbox_same_folder, window, selected_folder_pub_key):
    """
    Handles the document signature verification process.

    This function verifies the electronic signature in the selected PDF document. The result of the verification is displayed
    on the user interface. It returns a message indicating whether the verification was successful or failed.

    Parameters
    ----------
    status_label : QLabel
        The label in the user interface that provides status updates and prompts the user for further actions.
    app : QApplication
        The main application instance responsible for managing the application's event loop and updating the interface.
    checkbox_same_folder : QCheckBox
        The checkbox indicating whether the public key is located in the same folder as the private key on the USB device.
    window : QWidget
        The main application window used for displaying and interacting with the user interface.
    selected_folder_pub_key : str
        The folder path where the public key is located if it was selected by the user.

    Returns
    -------
    None.
    """
    try:
        status_label.setText("Weryfikacja podpisu...")
        status_label.setStyleSheet("""
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #FF6600;
            padding: 5px;
            border-radius: 5px;
            background-color: #FFF3E6;
            margin-top: 10px;
            font-weight: normal;
        """)
        app.processEvents()

        if checkbox_same_folder.isChecked():
            public_key = find_public_key(window.selected_pendrive)
            if not public_key:
                mess = f"Nie znaleziono klucza publicznego w {window.selected_pendrive}"
            else:
                mess = verify_signature(window.selected_file, public_key)
        else:
            if selected_folder_pub_key == "":
                mess = "Nie wybrano folderu z kluczem publicznym"
            else:
                public_key = find_public_key(selected_folder_pub_key)
                if not public_key:
                    mess = f"Nie znaleziono klucza publicznego w {selected_folder_pub_key}"
                else:
                    mess = verify_signature(window.selected_file, public_key)

        status_label.setText(mess)
        status_label.setStyleSheet("""
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #006600;
            padding: 5px;
            border-radius: 5px;
            background-color: #E6FFE6;
            margin-top: 10px;
            font-weight: normal;
        """)
    except Exception as e:
        status_label.setText(f"Błąd podczas weryfikacji podpisu: {str(e)}")
        status_label.setStyleSheet("""
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #CC0000;
            padding: 5px;
            border-radius: 5px;
            background-color: #FFEEEE;
            margin-top: 10px;
            font-weight: normal;
        """)


def create_gui():
    """
    Creates and runs the main window of the GUI application.

    This function sets up the user interface, including all widgets and event handling logic for file selection,
    USB drive detection, document signing, and signature verification. The application allows the user to choose a PDF
    file and a USB device, and then sign or verify a document.

    Parameters
    ----------
    None.

    Returns
    -------
    None.
    """
    app = QApplication(sys.argv)
    window = QWidget()

    window.setWindowIcon(QIcon('src/key.png'))
    window.setWindowTitle('Qualified Electronic Signature')
    window.setGeometry(100, 100, 700, 400)
    window.setWindowIcon(QIcon('src/assets/key.png'))

    window.selected_file = None
    window.selected_pendrive = None

    button_select_file = QPushButton('✧ Wybierz plik PDF ✧', window)
    file_preview = QTextEdit(window)
    file_preview.setReadOnly(True)
    file_preview.setPlaceholderText('📄 Podgląd pliku PDF...')

    status_label = QLabel('Wybierz plik PDF i nośnik USB', window)
    status_label.setAlignment(Qt.AlignCenter)
    status_label.setStyleSheet("""
        font-family: 'Verdana', sans-serif;
        font-size: 14px;
        color: #666666;
        padding: 5px;
        border-radius: 5px;
        background-color: #F0F0F0;
        margin-top: 10px;
        font-weight: normal;
    """)

    checkbox_same_folder = QCheckBox("Czy klucz publiczny i prywatny znajdują się w tym samym folderze?", window)
    checkbox_same_folder.setChecked(True)
    checkbox_same_folder.setVisible(False)

    selected_folder_pub_key = ""

    def handle_checkbox_change():
        if checkbox_same_folder.isChecked():
            pub_key_button.setDisabled(True)
        else:
            pub_key_button.setDisabled(False)

    button_select_file.clicked.connect(lambda: select_file(window, file_preview, status_label, button_sign_document, button_verify_signature, pub_key_button, checkbox_same_folder))
    checkbox_same_folder.clicked.connect(handle_checkbox_change)

    left_layout = QVBoxLayout()
    left_layout.addWidget(button_select_file)
    left_layout.addWidget(file_preview)

    usb_label = QLabel('🔌 Wykryte nośniki: ', window)
    usb_list = QListWidget(window)
    usb_list.setSelectionMode(QListWidget.SingleSelection)
    button_refresh_usb = QPushButton('🔄 Odśwież listę USB', window)

    button_refresh_usb.clicked.connect(lambda: refresh_usb(status_label, app, usb_list, window, button_sign_document, button_verify_signature, pub_key_button, checkbox_same_folder))

    button_sign_document = QPushButton('Podpisz dokument', window)
    button_sign_document.setVisible(False)

    button_verify_signature = QPushButton('Zweryfikuj podpis', window)
    button_verify_signature.setVisible(False)

    pub_key_button = QPushButton('Wybierz folder z kluczem publicznym', window)
    pub_key_button.setVisible(False)
    pub_key_button.setDisabled(True)

    usb_list.itemClicked.connect(lambda: select_usb_device(window, usb_list, button_sign_document, button_verify_signature, pub_key_button, checkbox_same_folder, status_label))
    button_sign_document.clicked.connect(lambda: sign_document(window, status_label, app))

    def select_folder_priv_pub_clicked():
        nonlocal selected_folder_pub_key
        selected_folder_pub_key = select_folder_pub_key(status_label, window)

    button_verify_signature.clicked.connect(lambda: signature_verification(status_label, app, checkbox_same_folder, window, selected_folder_pub_key))
    pub_key_button.clicked.connect(select_folder_priv_pub_clicked)

    right_layout = QVBoxLayout()
    right_layout.addWidget(usb_label)
    right_layout.addWidget(usb_list)
    right_layout.addWidget(button_refresh_usb)
    right_layout.addWidget(button_sign_document)
    right_layout.addWidget(button_verify_signature)
    right_layout.addWidget(pub_key_button)

    main_layout = QHBoxLayout()
    main_layout.addLayout(left_layout)
    main_layout.addLayout(right_layout)

    final_layout = QVBoxLayout()
    final_layout.addLayout(main_layout)
    final_layout.addWidget(status_label)

    window.setLayout(final_layout)

    right_layout.insertWidget(3, checkbox_same_folder)

    window.setStyleSheet("""
        QWidget {
            background-color: #ffff;
            font-family: 'Verdana', cursive, sans-serif;
        }
        QLabel {
            font-size: 16px;
            color: #b87d9a;
            padding: 10px;
            font-weight: semi-bold;
        }
        QPushButton {
            background-color: #edb2cf;
            color: white;
            border-radius: 15px;
            font-size: 16px;
            padding: 10px;
            margin-top: 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #b87d9a;
        }
        QPushButton:pressed {
            background-color: #7a4e64;
        }
        QPushButton:disabled {
            background-color: #adadad;
        }
        QTextEdit, QListWidget {
            background-color: white;
            border: 2px solid #7a4e64;
            border-radius: 10px;
            padding: 8px;
        }
    """)

    window.show()
    sys.exit(app.exec_())
