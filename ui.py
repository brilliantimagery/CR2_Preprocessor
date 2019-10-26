import os
import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QFileDialog, QPushButton, QLabel, QWidget


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.source_folder = None
        self.destination_folder = None

        self.setWindowTitle("DNG Converter")
        self.setGeometry(600, 300, 600, 300)

        self.make_exe_labels()

        self.make_button('Source Folder', self.set_source, 10, 50, 100, 30)
        self.make_button('Destination Folder', self.set_destination, 10, 80, 100, 30)



        button = QPushButton('test', self)
        button.setGeometry(100, 100, 100, 100)
        button.clicked.connect(self.print_stuff)

    def print_stuff(self):
        print(self.source_folder, self.destination_folder)

    def get_folder_closure(self, folder):
        def get_folder():
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.AnyFile)
            dialog.setViewMode(QFileDialog.List)
            if dialog.exec_():
                folder(dialog.selectedFiles())
        return get_folder

    def set_source(self, val):
        self.source_folder = val

    def set_destination(self, val):
        self.destination_folder = val

    def make_button(self, label, folder, x, y, w, h):
        button = QPushButton(label, self)
        button.setGeometry(x, y, w, h)
        dialog = self.get_folder_closure(folder)
        button.clicked.connect(dialog)

    def make_exe_labels(self):
        self.cr2hdr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dependencies', 'cr2hdr.exe')
        cr2hdr_path_label = QLabel(self)
        cr2hdr_path_label.setText(self.cr2hdr_path)
        cr2hdr_path_label.setGeometry(10, 10, 600, 10)
        cr2hdr_path_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)

        self.dng_converter_path = "C:\\Program Files (x86)\\Adobe\\Adobe DNG Converter.exe"
        dng_converter_path_label = QLabel(self)
        dng_converter_path_label.setText(self.dng_converter_path)
        dng_converter_path_label.setGeometry(10, 30, 600, 10)
        dng_converter_path_label.setAlignment(Qt.AlignBottom | Qt.AlignLeft)


app = QApplication(sys.argv)
window = Window()
window.show()

label = QLabel("<font color=red size=40>Hello World!</font>")

# label.show()

app.exec_()
sys.exit(0)

# from datetime import datetime
# import os
# from os import listdir
# from os.path import isfile, join
# import platform
# from subprocess import Popen, PIPE
# import shutil
# import time
#
#
# def get_creation_date(file):
#     if platform.system() == 'Windows':
#         return os.path.getctime(file)
#     else:
#         stat = os.stat(file)
#         try:
#             return stat.st_birthtime
#         except AttributeError:
#             # We're probably on Linux. No easy way to get creation dates here,
#             # so we'll settle for when its content was last modified.
#             return stat.st_mtime
#
#
# def get_datetime(file):
#     timestamp = get_creation_date(file)
#     return datetime.fromtimestamp(timestamp)
#
#
# def copy_files(files, destination_path):
#     folders = set()
#     for file in files:
#         capture_date = get_datetime(file)
#         year_path = os.path.join(destination_path, str(capture_date.year))
#         if not os.path.isdir(year_path):
#             os.mkdir(year_path)
#         day_path = os.path.join(year_path, str(capture_date)[:10])
#         if not os.path.isdir(day_path):
#             os.mkdir(day_path)
#         folders.add(day_path)
#         shutil.copyfile(file, os.path.join(day_path, os.path.basename(file)))
#
#     return folders
#
#
# def main():
#     t1 = datetime.now()
#     print('Starting:', t1)
#     cr2hdr_path = 'G:\\dual-iso\\cr2hdr.exe'
#     dng_converter_path = 'C:\\Program Files\\Adobe\Adobe DNG Converter\\Adobe DNG Converter.exe'
#     # "C:\Program Files\Adobe\Adobe DNG Converter\Adobe DNG Converter.exe" 'Adobe DNG Converter'
#     # "H:\\DCIM\\100CANON\\_MG_7886.DNG" "H:\\DCIM\\100CANON\\_MG_7886_2.DNG"
#     # source_path = 'F:\\Documents\\Python\\workflow'H:\DCIM\100CANON
#     source_path = 'H:\\DCIM\\100CANON'
#     source_path = 'G:\\Pictures\\2019\\2019-02-19'
#     destination_path = 'G:\\Pictures\\'
#
#     files_cr2 = [join(source_path, f) for f in listdir(source_path) if
#              isfile(join(source_path, f)) and f[-3:].lower() == 'cr2']
#
#     chunk_size = 16
#     for files in (files_cr2[pos:pos + chunk_size] for pos in range(0, len(files_cr2), chunk_size)):
#         processes = []
#         for file in files:
#             p = Popen(args=[cr2hdr_path, file], stdout=PIPE)
#             processes.append(p)
#         while True:
#             time.sleep(1)
#             finished = True
#             for process in processes:
#                 if process.poll() is None:
#                     finished = False
#             if finished:
#                 break
#
#     files_dng = [join(source_path, f) for f in listdir(source_path) if
#              isfile(join(source_path, f)) and f[-3:].lower() == 'dng']
#
#     for files in (files_dng[pos:pos + chunk_size] for pos in range(0, len(files_dng), chunk_size)):
#         processes = []
#         for file in files:
#             p = Popen(args=[dng_converter_path, '-c', file], stdout=PIPE)
#             processes.append(p)
#         while True:
#             time.sleep(1)
#             finished = True
#             for process in processes:
#                 if process.poll() is None:
#                     finished = False
#             if finished:
#                 break
#
#     for file in files_dng:
#         os.remove(file)
#         os.rename(file[:-4] + '_1.dng', file[:-4] + '.dng')
#
#     print('Finished:', datetime.now(), t1 - datetime.now())
#
#
#
#     # files = [join(source_path, f) for f in listdir(source_path) if
#     #          isfile(join(source_path, f)) and f[-3:].lower() == 'cr2']
#     #
#     # folders = copy_files(files, destination_path)
#     # print('folders', folders)
#     #
#     # for folder in folders:
#     #     print('folder', folder)
#     #     files = [join(folder, f) for f in listdir(folder) if
#     #              isfile(join(folder, f)) and f[-3:].lower() == 'cr2']
#     #     for file in files:
#     #         cr2hdr_process = Popen([cr2hdr_path, file])
#     #
#     #     while True:
#     #         print('checking')
#     #         n_files = len(listdir(folder))
#     #         time.sleep(60)
#     #         print(n_files == len(listdir(folder)), n_files, len(listdir(folder)))
#     #         if n_files == len(listdir(folder)):
#     #             pring('do')
#     #             break
#     #
#     #     files = sorted([join(folder, f)[:-3] for f in listdir(folder) if isfile(join(folder, f))])
#     #     print('0000000', files)
#     #     # files_to_delete = []
#     #     for index, file in enumerate(files[:-1]):
#     #         if file[:-3] == files[index+1][:-3]:
#     #             os.remove(file)
#     #         # files_to_delete.append(file)
#
#     # cr2hdr_process = Popen([cr2hdr_path, 'H:\\DCIM\\100CANON\\_MG_7886.CR2'], stdout=PIPE)
#     # print(cr2hdr_process)
#     # dng_converter_process = Popen([dng_converter_path, '-c', 'H:\\DCIM\\100CANON\\_MG_7886.DNG'])
#
#
# if __name__ == '__main__':
#     main()
#
