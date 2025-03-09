import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

from key_generation import key_generator


def create_gui():
    app = QApplication(sys.argv)
    window = QWidget()

    window.setWindowIcon(QIcon('src/assets/key.png'))
    window.setWindowTitle('Generowanie Kluczy RSA')
    window.setGeometry(100, 100, 700, 400)

    selected_folder = ""
    pin = ""

    def select_folder():
        nonlocal selected_folder
        folder_path = QFileDialog.getExistingDirectory(window, 'Wybierz folder do zapisania kluczy', '')
        if folder_path:
            selected_folder = folder_path
            folder_label.setText(f"Ścieżka wybranego folderu: {folder_path}")
            folder_label.setStyleSheet("""
                QLabel {
                    font-family: 'Verdana', sans-serif;
                    font-size: 14px;
                    color: #D5006B;
                    padding-left: 10px;
                    padding-top: 5px;
                    font-style: italic;
                }
            """)

    def generate_rsa():
        nonlocal pin
        pin = pin_input.text()

        if not pin.isdigit():
            QMessageBox.warning(window, "Błąd", "PIN musi składać się tylko z cyfr.")
            return

        if pin and selected_folder:
            key_generator(pin, selected_folder)
            print(f"Generowanie kluczy RSA z PIN-em: {pin}")
            QMessageBox.information(window, "Sukces", f"Klucze RSA zostały wygenerowane w folderze: {selected_folder}")
        else:
            QMessageBox.warning(window, "Błąd", "Proszę wprowadzić PIN i wybrać folder.")

    layout = QVBoxLayout()

    folder_layout = QVBoxLayout()
    folder_label_title = QLabel("Wybierz folder do zapisania kluczy", window)
    folder_label_title.setStyleSheet("""
        QLabel {
            font-family: 'Arial', sans-serif;
            font-size: 18px;
            color: #D5006B;
            padding-bottom: 10px;
            font-weight: bold;
        }
    """)

    button_select_folder = QPushButton('Wybierz folder', window)
    button_select_folder.clicked.connect(select_folder)
    button_select_folder.setStyleSheet("""
        QPushButton {
            background-color: #ff7fae;
            color: white;
            border-radius: 15px;
            font-size: 16px;
            padding: 10px;
            margin-top: 10px;
        }
        QPushButton:hover {
            background-color: #ff467f;
        }
        QPushButton:pressed {
            background-color: #e72d5f;
        }
    """)

    folder_label = QLabel("Ścieżka folderu: Nie wybrano", window)
    folder_label.setStyleSheet("""
        QLabel {
            font-family: 'Verdana', sans-serif;
            font-size: 14px;
            color: #D5006B;
            padding-left: 10px;
            padding-top: 5px;
            font-style: italic;
        }
    """)

    folder_layout.addWidget(folder_label_title)
    folder_layout.addWidget(button_select_folder)
    folder_layout.addWidget(folder_label)

    pin_input = QLineEdit(window)
    pin_input.setEchoMode(QLineEdit.Password)
    pin_input.setPlaceholderText("Wpisz PIN")
    pin_input.setStyleSheet("""
        QLineEdit {
            font-family: 'Verdana', sans-serif;
            font-size: 20px;
            text-align: center;
            padding: 10px;
            border: 2px solid #ff7fae;
            border-radius: 10px;
            margin-top: 20px;
        }
    """)

    button_generate_rsa = QPushButton('Generuj RSA', window)
    button_generate_rsa.setStyleSheet("""
        QPushButton {
            background-color: #ff7fae;
            color: white;
            border-radius: 15px;
            font-size: 18px;
            padding: 15px;
            margin-top: 20px;
        }
        QPushButton:hover {
            background-color: #ff467f;
        }
        QPushButton:pressed {
            background-color: #e72d5f;
        }
    """)
    button_generate_rsa.clicked.connect(generate_rsa)

    layout.addLayout(folder_layout)
    layout.addWidget(pin_input)
    layout.addWidget(button_generate_rsa)

    window.setLayout(layout)

    window.setStyleSheet("""
        QWidget {
            background-color: #fff0f5;
            font-family: 'Verdana', cursive, sans-serif;
        }
    """)

    window.show()
    sys.exit(app.exec_())
