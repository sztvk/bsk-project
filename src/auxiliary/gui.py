import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QFileDialog, QListWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from key_generation import key_generator
from src.detecting_usb import detect_usb_devices


def create_gui():
    """
    Creates the graphical user interface (GUI) for the RSA key generation application.
    It allows the user to select a folder, enter a PIN, and generate RSA keys.

    The GUI includes the following components:
    - A folder selection dialog for saving the keys.
    - A PIN input field for entering a security PIN.
    - A button to trigger the RSA key generation process.
    - A status label to display messages to the user.

    Returns
    -------
    None
    """
    app = QApplication(sys.argv)
    window = QWidget()

    selected_usb_priv_key = ""
    selected_folder_pub_key = ""
    pin = ""

    window.setWindowIcon(QIcon('src/assets/key.png'))
    window.setWindowTitle('Generowanie Kluczy RSA')
    window.setGeometry(100, 100, 700, 400)

    layout = QVBoxLayout()

    folder_layout = QVBoxLayout()

    folder_label_title = QLabel("Wybierz miejsca zapisu kluczy", window)
    folder_label_title.setStyleSheet("""
           font-weight: bold;
           font-size: 16px;
           text-decoration: underline;
       """)

    private_key_label = QLabel("Klucz prywatny", window)
    private_key_label.setStyleSheet("""
        font-weight: bold;
        font-size: 14px;
    """)

    public_key_label = QLabel("Klucz publiczny", window)
    public_key_label.setStyleSheet("""
            font-weight: bold;
            font-size: 14px;
        """)

    folder_label = QLabel("Ścieżka folderu: Nie wybrano", window)
    folder_label.setStyleSheet("""
            font-size: 12px;
        """)

    folder_pub_label = QLabel("Ścieżka folderu: Nie wybrano", window)
    folder_pub_label.setStyleSheet("""
        font-size: 12px;
    """)

    key_label_title = QLabel("Wygeneruj klucze")
    key_label_title.setStyleSheet("""
               font-weight: bold;
               font-size: 16px;
               text-decoration: underline;
           """)

    status_label = QLabel("Wybierz folder i wprowadź PIN", window)
    status_label.setStyleSheet("""
        QLabel {
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #666666;
            padding: 5px;
            border-radius: 5px;
            background-color: #F0F0F0;
            margin-top: 10px;
        }
    """)
    status_label.setAlignment(Qt.AlignCenter)

    usb_list = QListWidget(window)

    button_refresh_usb = QPushButton('🔄 Odśwież listę USB', window)


    button_select_folder_pub_key = QPushButton('📜 Wybierz folder dla klucza publicznego', window)


    pin_input = QLineEdit(window)
    pin_input.setEchoMode(QLineEdit.Password)
    pin_input.setPlaceholderText("Wpisz PIN")

    button_generate_rsa = QPushButton('🔑 Generuj RSA', window)

    def refresh_usb():
        """
        Refreshes the list of detected USB devices.

        This function searches for connected USB devices and updates the list in the user interface. It provides status updates
        to the user, indicating whether devices were detected or if no devices were found. If devices are detected, the user
        can select one from the list, which will then enable the functionality to sign or verify the document.

        Parameters
        ----------
        None.

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

    def select_folder_priv_key():
        """
        Selects a USB device for storing the private key.

        Retrieves the selected item from the USB device list and saves it as the path
        for the private key. Updates the UI labels accordingly.

        If the public key folder has not been selected, the user is prompted to choose one.

        Returns
        -------
        None
        """
        nonlocal selected_usb_priv_key
        selected_usb_priv_key = usb_list.currentItem().text()

        if selected_usb_priv_key:
            folder_label.setText(f"Ścieżka wybranego folderu: {selected_usb_priv_key}")
            if selected_folder_pub_key:
                status_label.setText("Folder wybrany. Wprowadź PIN i kliknij 'Generuj RSA'")
            else:
                status_label.setText("Wybierz folder dla klucza publicznego")

    def select_folder_pub_key():
        """
        Selects a folder for storing the public key.

        Opens a file dialog allowing the user to select a directory to save the public key.
        Updates the UI labels accordingly.

        If the USB device for the private key has not been selected, the user is prompted to do so.

        Returns
        -------
        None
        """
        nonlocal selected_folder_pub_key
        folder_path_pub_key = QFileDialog.getExistingDirectory(window, 'Wybierz folder do zapisania klucza publicznego')
        if folder_path_pub_key:
            selected_folder_pub_key = folder_path_pub_key
            folder_pub_label.setText(f"Ścieżka wybranego folderu: {folder_path_pub_key}")
            if selected_usb_priv_key != "":
                status_label.setText("Foldery wybrane. Wprowadź PIN i kliknij 'Generuj RSA'")
            else:
                status_label.setText("Wybierz urządzenie USB dla klucza prywatnego")
            status_label.setStyleSheet("""
                QLabel {
                    font-family: 'Verdana', sans-serif;
                    font-size: 14px;
                    color: #0066CC;
                    padding: 5px;
                    border-radius: 5px;
                    background-color: #E6F2FF;
                    margin-top: 10px;
                }
            """)

    def generate_rsa():
        """
        Generates RSA keys using the provided PIN and saves them to the selected folder.
        Validates user input, including checking if the PIN is a valid numeric value and if a folder is selected.

        If the key generation process is successful, the status label is updated to inform the user.
        If there is an error, an error message is displayed.

        Returns
        -------
        None
        """
        nonlocal pin
        pin = pin_input.text()

        if not pin.isdigit():
            status_label.setText("Błąd! PIN musi składać się tylko z cyfr.")
            status_label.setStyleSheet("""
                QLabel {
                    font-family: 'Verdana', sans-serif;
                    font-size: 14px;
                    color: #CC0000;
                    padding: 5px;
                    border-radius: 5px;
                    background-color: #FFEEEE;
                    margin-top: 10px;
                }
            """)
            return

        if not selected_usb_priv_key or not selected_folder_pub_key:
            status_label.setText("Błąd! Nie wybrano folderu do zapisania kluczy.")
            status_label.setStyleSheet("""
                QLabel {
                    font-family: 'Verdana', sans-serif;
                    font-size: 14px;
                    color: #CC0000;
                    padding: 5px;
                    border-radius: 5px;
                    background-color: #FFEEEE;
                    margin-top: 10px;
                }
            """)
            return

        if not pin:
            status_label.setText("Błąd! Nie wprowadzono PIN-u.")
            status_label.setStyleSheet("""
                QLabel {
                    font-family: 'Verdana', sans-serif;
                    font-size: 14px;
                    color: #CC0000;
                    padding: 5px;
                    border-radius: 5px;
                    background-color: #FFEEEE;
                    margin-top: 10px;
                }
            """)
            return

        status_label.setText("Generowanie kluczy RSA w toku...")
        status_label.setStyleSheet("""
            QLabel {
                font-family: 'Verdana', sans-serif;
                font-size: 14px;
                color: #FF6600;
                padding: 5px;
                border-radius: 5px;
                background-color: #FFF3E6;
                margin-top: 10px;
            }
        """)

        app.processEvents()

        try:
            key_generator(pin, selected_usb_priv_key, selected_folder_pub_key)
            print(f"Generowanie kluczy RSA z PIN-em: {pin}")
            status_label.setText(
                f"Sukces! Klucze prywatny został zapisany w folderze: {selected_usb_priv_key}, a klucz publiczny w {selected_folder_pub_key}")
            status_label.setStyleSheet("""
                QLabel {
                    font-family: 'Verdana', sans-serif;
                    font-size: 14px;
                    color: #006600;
                    padding: 5px;
                    border-radius: 5px;
                    background-color: #E6FFE6;
                    margin-top: 10px;
                }
            """)
            pin_input.clear()
        except Exception as e:
            status_label.setText(f"Błąd podczas generowania kluczy: {str(e)}")
            status_label.setStyleSheet("""
                QLabel {
                    font-family: 'Verdana', sans-serif;
                    font-size: 14px;
                    color: #CC0000;
                    padding: 5px;
                    border-radius: 5px;
                    background-color: #FFEEEE;
                    margin-top: 10px;
                }
            """)

    button_refresh_usb.clicked.connect(refresh_usb)
    usb_list.itemClicked.connect(select_folder_priv_key)
    button_select_folder_pub_key.clicked.connect(select_folder_pub_key)
    button_generate_rsa.clicked.connect(generate_rsa)

    folder_layout.addWidget(folder_label_title)
    folder_layout.addWidget(private_key_label)
    folder_layout.addWidget(usb_list)
    folder_layout.addWidget(button_refresh_usb)
    folder_layout.addWidget(folder_label)
    folder_layout.addWidget(public_key_label)
    folder_layout.addWidget(button_select_folder_pub_key)
    folder_layout.addWidget(folder_pub_label)

    layout.addLayout(folder_layout)
    layout.addWidget(key_label_title)
    layout.addWidget(pin_input)
    layout.addWidget(button_generate_rsa)
    layout.addWidget(status_label)

    window.setStyleSheet("""
            QWidget {
                background-color: #ffff;
                font-family: 'Verdana', cursive, sans-serif;
            }
            QLabel {
                font-size: 16px;
                color: #b87d9a;
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
             QLineEdit {
                background-color: white;
                border: 2px solid #7a4e64;
                border-radius: 10px;
                padding: 8px;
                font-size: 16px;
                color: #333;
            }
            QLineEdit:focus {
                border: 2px solid #b87d9a;
                background-color: #fff5fa;
            }
            QTextEdit, QListWidget {
                background-color: white;
                border: 2px solid #7a4e64;
                border-radius: 10px;
                padding: 8px;
            }
        """)

    window.setLayout(layout)
    window.show()

    sys.exit(app.exec_())