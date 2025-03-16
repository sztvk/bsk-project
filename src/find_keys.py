import os


def find_public_key(directory):
    for root, _, files in os.walk(directory):
        if "public_key.pubk" in files:
            return os.path.join(root, "public_key.pubk")
    return None


def find_private_key(directory):
    for root, _, files in os.walk(directory):
        if "encrypted_private_key.pk" in files:
            return os.path.join(root, "encrypted_private_key.pk")
    return None


def main():
    directory = input("Ścieżka pendrive: ")
    public_key = find_public_key(directory)
    private_key = find_private_key(directory)
    print(public_key, private_key)


if __name__ == '__main__':
    main()
