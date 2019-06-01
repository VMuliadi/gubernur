import os
import plyvel

kube_magic_word = os.getenv("KUBECONFIG_MAGIC_WORD")
database = plyvel.DB("./database", create_if_missing=True)


def put_item(kubeconfig_file, client_name):
    """
    Add padding to the original byte file and put it to the LevelDB
    :param kubeconfig_file:  kubeconfig file (file)
    :param client_name: the client name (string)
    :return: None
    """
    bytes_version = bytes()
    with open(kubeconfig_file, 'rb') as kubeconfig:
        for byte in iter(lambda: kubeconfig.read(1), b''):
            bytes_version = bytes_version + byte
    bytes_version = kube_magic_word.encode() + bytes_version
    database.put(bytes(client_name, "utf-8"), bytes_version)


def get_kubeconfig_to_leveldb(client_name):
    """
    Remove padding from the kubeconfig file and return it in byte format
    :param client_name: the client name (string)
    :return: the true value of kubeconfig from leveldb after remove the padding (byte)
    """
    kubeconfig = database.get(bytes(client_name, "utf-8")).decode()
    return kubeconfig.replace(kube_magic_word, "", 1).encode()
