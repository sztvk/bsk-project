import os


def find_keys(directory):
    public_key_path = None
    encrypted_private_key_path = None

    for root, _, files in os.walk(directory):
        if "public_key.pubk" in files:
            public_key_path = os.path.join(root, "public_key.pubk")
        if "encrypted_private_key.pk" in files:
            encrypted_private_key_path = os.path.join(root, "encrypted_private_key.pk")

        if public_key_path and encrypted_private_key_path:
            break

    return public_key_path, encrypted_private_key_path


def main():
    directory = input("Ścieżka pendrive: ")
    public_key, private_key = find_keys(directory)
    print(public_key, private_key)


if __name__ == '__main__':
    main()
