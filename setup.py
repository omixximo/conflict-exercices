from os import makedirs, getcwd
from os.path import isdir, join

N_FOLDERS = 5
N_FILES = 3
N_LINES = 10

MAIN_FOLDER_NAME = 'folders'
FOLDER_NAME = 'folder_{folder_number}'
FILE_NAME = 'file_{folder_number}_{file_number}'
LINES_TEST = 'line_{line_number} 0'

def create_folder(path):
    if not isdir(path):
        makedirs(path)

def main():
    cwd = getcwd()
    main_folder_path = join(cwd, MAIN_FOLDER_NAME)
    create_folder(main_folder_path)

    for folder_number in range(N_FOLDERS):
        folder_name = FOLDER_NAME.format(folder_number = folder_number)
        folder_path = join(main_folder_path, folder_name)
        create_folder(folder_path)
        for file_number in range(N_FILES):
            file_name = FILE_NAME.format(folder_number = folder_number, file_number = file_number)
            file_path = join(folder_path, file_name)
            with open(file_path, mode = 'w') as f:
                for line_number in range(N_LINES):
                    f.write(LINES_TEST.format(folder_number = folder_number, file_number = file_number, line_number = line_number) + '\n')

if __name__ == '__main__':
    main()