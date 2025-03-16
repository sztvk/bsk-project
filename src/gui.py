import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QListWidget, QMessageBox, QTextEdit, QInputDialog
from PyQt5.QtGui import QIcon

from src.detecting_usb import detect_usb_devices
from src.document_signing import sign_pdf
from src.find_keys import find_public_key
from src.verify_signature import verify_signature


def create_gui():
    app = QApplication(sys.argv)
    window = QWidget()

    window.setWindowIcon(QIcon('src/key.png'))
    window.setWindowTitle('Qualified Electronic Signature')
    window.setGeometry(100, 100, 700, 400)
    window.setWindowIcon(QIcon('src/assets/key.png'))

    window.selected_file = None
    window.selected_pendrive = None

    button_select_file = QPushButton('💖 Wybierz plik PDF 💖', window)
    file_preview = QTextEdit(window)
    file_preview.setReadOnly(True)
    file_preview.setPlaceholderText('📄 Podgląd pliku PDF...')

    def select_file():
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(window, 'Wybierz plik PDF', '', 'PDF Files (*.pdf)')
        if file_path:
            file_path = file_path.replace("/", "\\")
            window.selected_file = file_path
            file_preview.setText(f'📜 Wybrany plik: {file_path}')

    button_select_file.clicked.connect(select_file)

    left_layout = QVBoxLayout()
    left_layout.addWidget(button_select_file)
    left_layout.addWidget(file_preview)

    usb_label = QLabel('🔌 Wykryte nośniki: ', window)
    usb_list = QListWidget(window)
    usb_list.setSelectionMode(QListWidget.SingleSelection)
    button_refresh_usb = QPushButton('🔄 Odśwież listę USB', window)

    def refresh_usb():
        usb_list.clear()
        devices = detect_usb_devices()
        usb_list.addItems([f"{dev}" for dev in devices])

    button_refresh_usb.clicked.connect(refresh_usb)

    button_sign_document = QPushButton('Podpisz dokument', window)
    button_sign_document.setVisible(False)

    button_verify_signature = QPushButton('Zweryfikuj podpis', window)
    button_verify_signature.setVisible(False)

    def on_item_clicked():
        window.selected_pendrive = usb_list.currentItem().text()

        button_sign_document.setVisible(True)
        button_verify_signature.setVisible(True)

    usb_list.itemClicked.connect(on_item_clicked)

    def sign_document():
        pin, ok = QInputDialog.getText(window, 'Wprowadź PIN', 'Podaj PIN do klucza:')

        if ok and pin:
            try:
                pin = str(pin)
                sign_pdf(window.selected_pendrive, window.selected_file, pin)
            except ValueError:
                QMessageBox.warning(window, 'Błąd', 'Nieprawidłowy PIN.')
        else:
            QMessageBox.warning(window, 'Błąd', 'PIN nie został wprowadzony.')

    button_sign_document.clicked.connect(sign_document)

    def signature_verification():
        public_key = find_public_key(window.selected_pendrive)
        verify_signature(window.selected_file, public_key)

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

    window.setLayout(main_layout)

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
