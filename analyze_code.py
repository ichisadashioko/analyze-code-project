import os
import time
import json

import numpy as np
import matplotlib.pyplot as plt
from binaryornot.check import is_binary


class NodeInstance:
    def __init__(self, path: str):
        self.path = path
        self.name = os.path.basename(path)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class FileInstance(NodeInstance):
    def __init__(self, path: str):
        NodeInstance.__init__(self, path)

        self.extension = os.path.splitext(path)[1]
        self.size = os.path.getsize(path)


class TextFileInstance(FileInstance):
    def __init__(self, path: str):
        FileInstance.__init__(self, path)

        self.line_count = sum(1 for line in open(path))


class BinFileInstance(FileInstance):
    def __init__(self, path: str):
        FileInstance.__init__(self, path)


class DirectoryInstance(NodeInstance):
    def __init__(self, path: str, children=[]):
        NodeInstance.__init__(self, path)

        self.children = children


ignore_files = [
    '.git',
    '.vs',
    'bin',
    'obj',
    'packages',
]

file_format = {
    'extension': '.js',
    'type': 'text|bin',
    'size': 1024,
    'line_count': 32,
}


def build_file_tree(path: str):

    if os.path.isfile(path):
        if is_binary(path):
            return BinFileInstance(path)
        else:
            return TextFileInstance(path)
    else:
        file_list = os.listdir(path)
        children = list(map(lambda child_file: f'{path}/{child_file}', file_list))
        children = list(map(lambda child: build_file_tree(child), children))

        return DirectoryInstance(path, children)


def print_binary_files(path):
    base_name = os.path.basename(path)
    if base_name in ignore_files:
        return

    if os.path.isfile(path):
        if is_binary(path):
            print(path)
    else:
        file_list = os.listdir(path)
        for child_name in file_list:
            child_path = f'{path}/{child_name}'
            print_binary_files(child_path)


if __name__ == '__main__':
    root_dir = '.'
    # print_binary_files(root_dir)
    file_tree = build_file_tree(root_dir)
    print(file_tree.toJSON())
