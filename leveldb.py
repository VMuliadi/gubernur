import os
import plyvel
database = plyvel.DB('./database', create_if_missing=True)


def put_kubeconfig_to_leveldb(kubeconfig):
    bytes_version = bytes()
    with open(kubeconfig, 'rb') as filestream:
        byte = filestream.read(1)
        while byte:
            byte = filestream.read(1)
            bytes_version = bytes_version + byte
    database.put(bytes(kubeconfig.split('/')[-1], 'utf-8'), bytes_version)
    return kubeconfig.split('/')[-1]


def get_kubeconfig_to_leveldb(kubeconfig):
    return database.get(bytes(kubeconfig.split('/')[-1], 'utf-8'))


key = put_kubeconfig_to_leveldb(os.path.abspath('./README.md'))
print(get_kubeconfig_to_leveldb(key))
