import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QListWidget, QMessageBox, QTextEdit, QInputDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from src.detecting_usb import detect_usb_devices
from src.document_signing import sign_pdf
from src.find_keys import find_public_key
from src.verify_signature import verify_signature


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

    def select_file():
        """
        Opens a dialog to select a PDF file and displays its path in the widget.

        This function allows the user to choose a PDF file, and then updates the file preview widget and the status in the GUI.
        Once both a file and a USB drive are selected, the user can sign or verify the document.

        Parameters
        ----------
        None.

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

    button_select_file.clicked.connect(select_file)

    left_layout = QVBoxLayout()
    left_layout.addWidget(button_select_file)
    left_layout.addWidget(file_preview)

    usb_label = QLabel('🔌 Wykryte nośniki: ', window)
    usb_list = QListWidget(window)
    usb_list.setSelectionMode(QListWidget.SingleSelection)
    button_refresh_usb = QPushButton('🔄 Odśwież listę USB', window)

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
        button_sign_document.setVisible(False)
        button_verify_signature.setVisible(False)

    button_refresh_usb.clicked.connect(refresh_usb)

    button_sign_document = QPushButton('Podpisz dokument', window)
    button_sign_document.setVisible(False)

    button_verify_signature = QPushButton('Zweryfikuj podpis', window)
    button_verify_signature.setVisible(False)

    def on_item_clicked():
        """
        Handles the selection of a USB device from the list.

        This function sets the selected USB device and updates the interface widgets, including enabling the buttons for
        signing and verifying the document. The status is also updated based on the selection.

        Parameters
        ----------
        None.

        Returns
        -------
        None.
        """
        window.selected_pendrive = usb_list.currentItem().text()

        if window.selected_file and window.selected_pendrive:
            button_sign_document.setVisible(True)
            button_verify_signature.setVisible(True)
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

    usb_list.itemClicked.connect(on_item_clicked)

    def sign_document():
        """
        Handles the document signing process.

        This function opens a dialog to input the PIN, then processes the selected PDF file using the private key from the
        selected USB device. The user interface status is updated during the signing process.

        Parameters
        ----------
        None.

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

    button_sign_document.clicked.connect(sign_document)

    def signature_verification():
        """
        Handles the document signature verification process.

        This function verifies the electronic signature in the selected PDF document. The result of the verification is displayed
        on the user interface. It returns a message indicating whether the verification was successful or failed.

        Parameters
        ----------
        None.

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

            public_key = find_public_key(window.selected_pendrive)
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

    button_verify_signature.clicked.connect(signature_verification)

    right_layout = QVBoxLayout()
    right_layout.addWidget(usb_label)
    right_layout.addWidget(usb_list)
    right_layout.addWidget(button_refresh_usb)
    right_layout.addWidget(button_sign_document)
    right_layout.addWidget(button_verify_signature)

    main_layout = QHBoxLayout()
    main_layout.addLayout(left_layout)
    main_layout.addLayout(right_layout)

    final_layout = QVBoxLayout()
    final_layout.addLayout(main_layout)
    final_layout.addWidget(status_label)

    window.setLayout(final_layout)

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
        QTextEdit, QListWidget {
            background-color: white;
            border: 2px solid #7a4e64;
            border-radius: 10px;
            padding: 8px;
        }
    """)

    window.show()
    sys.exit(app.exec_())
