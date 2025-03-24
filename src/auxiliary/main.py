from src.auxiliary.gui import create_gui

def main():
    """
    Main function to run the RSA key generation GUI application.

    This function calls `create_gui()` to initialize and start the graphical user interface
    for generating RSA keys. The GUI allows users to select a folder, enter a PIN, and generate keys.

    Parameters
    ----------
    None.

    Returns
    -------
    None
    """
    create_gui()


if __name__ == '__main__':
    main()
