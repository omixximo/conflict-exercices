import argparse

from os import makedirs, getcwd
from os.path import isdir, join

from typing import Tuple, Collection

N_FOLDERS = 5
N_FILES = 3
N_LINES = 10

MAIN_FOLDER_NAME = 'folders'
FOLDER_NAME = 'folder_{folder_number}'
FILE_NAME = 'file_{folder_number}_{file_number}'
INITIAL_LINE_TEXT_WITHOUT_SUBLINE = 'line_{line_number}'
INITIAL_LINE_TEXT = INITIAL_LINE_TEXT_WITHOUT_SUBLINE + '.{subline_number}'
LINES_TEXT_SEPARATOR = ' -> '
LINES_TEXT_WIWHOUT_SUBLINE = INITIAL_LINE_TEXT_WITHOUT_SUBLINE + LINES_TEXT_SEPARATOR + '{feature}'
LINES_TEXT = INITIAL_LINE_TEXT + LINES_TEXT_SEPARATOR + '{feature}'

DEFAULT_FEATURE = '0'

cwd = getcwd()
main_folder_path = join(cwd, MAIN_FOLDER_NAME)

def format_line_start(folder_number,  file_number, line_number, subline_number=0) -> str:
    if subline_number != 0:
        return INITIAL_LINE_TEXT.format(folder_number=folder_number, file_number=file_number, line_number=line_number, subline_number=0)
    else:
        return INITIAL_LINE_TEXT_WITHOUT_SUBLINE.format(folder_number=folder_number, file_number=file_number, line_number=line_number, subline_number=0)

def format_line(folder_number,  file_number, line_number, subline_number=0, feature=DEFAULT_FEATURE) -> str:
    if subline_number != 0:
        return LINES_TEXT.format(folder_number=folder_number, file_number=file_number, line_number=line_number, subline_number=subline_number, feature=feature)
    else:
        return LINES_TEXT_WIWHOUT_SUBLINE.format(folder_number=folder_number, file_number=file_number, line_number=line_number, subline_number=subline_number, feature=feature)

# {feature_name} [{change_code}]
# changecode = '3.1.6.0'
class Change():

    folder :int
    file :int
    line :int
    subline :int

    feature :str

    def __init__(self, code :str, feature :str):
        split_code :Tuple[int, ...] = tuple(int(x) for x in code.split('.'))
        self.folder, self.file, self.line, self.subline = split_code
        self.feature = feature

    def apply(self) -> None:
        file_content = None
        file_path = get_file(self.folder, self.file)
        with open(file_path, mode='r') as f:
            file_content = f.read()
        
        final_lines :list[str] = []
        line_start = format_line_start(self.folder, self.file, self.line, subline_number=self.subline)
        previous_lines : Collection[str] = {format_line_start(self.folder, self.file, self.line, subline_number=previous_subline) for previous_subline in range(self.subline)} if self.subline > 0 else {}
        found_line = False
        
        for line in file_content.split('\n'):
            initial, *_ = line.split(LINES_TEXT_SEPARATOR)
            if initial == line_start:
                line = format_line(self.folder, self.file, self.line, subline_number=self.subline, feature=self.feature)
            elif initial in previous_lines:
                found_line = True
            elif found_line:
                found_line = False
                final_lines.append(format_line(self.folder, self.file, self.line, subline_number=self.subline, feature=self.feature))
            final_lines.append(line)

        with open(file_path, mode = 'w') as f:
            print('\n'.join(final_lines))
            f.write('\n'.join(final_lines))

        with open(file_path, mode='r') as f:
            print(f.read())

    def __str__(self) -> str:
        return f'{self.folder}.{self.file}.{self.line}.{self.subline}'
    def __repr__(self) -> str:
        return f'Change({str(self)})'
    
class Order():
    
    feature :str
    changes :list[Change]

    def __init__(self, order_str :str):
        split_order = order_str.split()
        self.feature = split_order[0]
        self.changes = [Change(code, self.feature) for code in split_order[1:]]

    def apply_changes(self) -> None:
        for change in self.changes:
            change.apply()

def create_folder(path :str) -> None:
    if not isdir(path):
        makedirs(path)

def get_file(folder_number :int, file_number :int) -> str:
    folder_name = FOLDER_NAME.format(folder_number = folder_number)
    file_name = FILE_NAME.format(folder_number = folder_number, file_number = file_number)
    return join(main_folder_path, folder_name, file_name)

def setup(*args) -> None:

    create_folder(main_folder_path)

    for folder_number in range(1, N_FOLDERS+1):
        folder_name = FOLDER_NAME.format(folder_number=folder_number)
        folder_path = join(main_folder_path, folder_name)
        create_folder(folder_path)
        for file_number in range(1, N_FILES+1):
            file_name = FILE_NAME.format(folder_number=folder_number, file_number=file_number)
            file_path = join(folder_path, file_name)
            with open(file_path, mode='w') as f:
                for line_number in range(1, N_LINES+1):
                    f.write(format_line(folder_number, file_number, line_number) + '\n')

def main() -> None:
    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, description='Action', help='Choose action to execute.')

    def update(args):
        for order in args.orders:
            Order(order).apply_changes()

    # create the parser for the "setup" command
    parser_setup = subparsers.add_parser('setup', description='Setups folders and files to start position')
    parser_setup.set_defaults(func=setup)

    # create the parser for the "bar" command
    parser_bar = subparsers.add_parser('update')
    parser_bar.add_argument('orders', nargs='+')
    parser_bar.set_defaults(func=update)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()