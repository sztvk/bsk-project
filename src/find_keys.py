import os


def find_public_key(directory):
    """
    Finds the public key file (`public_key.pubk`) in the specified directory and its subdirectories.

    This function searches through the directory and its subdirectories to find a file named `public_key.pubk`.
    If the file is found, the full path to the file is returned. Otherwise, `None` is returned.

    Parameters
    ----------
    directory : str
        The path to the directory where the search for the public key will be performed.

    Returns
    -------
    str or None
        The full path to the public key file if found, otherwise `None`.
    """
    for root, _, files in os.walk(directory):
        if "public_key.pubk" in files:
            return os.path.join(root, "public_key.pubk")
    return None


def find_private_key(directory):
    """
    Finds the private key file (`encrypted_private_key.pk`) in the specified directory and its subdirectories.

    This function searches through the directory and its subdirectories to find a file named `encrypted_private_key.pk`.
    If the file is found, the full path to the file is returned. Otherwise, `None` is returned.

    Parameters
    ----------
    directory : str
        The path to the directory where the search for the private key will be performed.

    Returns
    -------
    str or None
        The full path to the private key file if found, otherwise `None`.
    """
    for root, _, files in os.walk(directory):
        if "encrypted_private_key.pk" in files:
            return os.path.join(root, "encrypted_private_key.pk")
    return None
