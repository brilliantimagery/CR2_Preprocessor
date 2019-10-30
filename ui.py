import datetime
import multiprocessing
import os
from shutil import copy2
from subprocess import Popen, PIPE, check_output
import sys
import time

from PySide2.QtCore import Qt, QObject
from PySide2.QtWidgets import QApplication, QFileDialog, QPushButton, QLabel, QWidget


def _wait(processes, chunk_size):
    while True:
        processes = [p for p in processes if p.poll() is None]
        if len(processes) >= chunk_size and processes:
            time.sleep(1)
        else:
            break

    return processes


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.source_folder = None
        self.destination_folder = None

        self.setWindowTitle("DNG Converter")
        self.setGeometry(600, 300, 600, 300)

        self._make_exe_labels()

        self._make_folder_button('Source Folder', self._set_source, 10, 50, 100, 30)
        self._make_folder_button('Destination Folder', self._set_destination, 10, 80, 100, 30)
        self._make_submit_button('Process', 10, 110, 100, 30)

    def _get_folder__closure(self, folder):
        def get_folder():
            dir = QFileDialog.getExistingDirectory(self, dir='C:\\Users\\chadd\\Desktop\\test_images')
            folder(dir)

        return get_folder

    def _set_source(self, val):
        # self.source_folder = self._process_selection(val)
        self.source_folder = val

    def _set_destination(self, val):
        # self.destination_folder = self._process_selection(val)
        self.destination_folder = val

    def _process_selection(self, val):
        # val = val[0]
        # if os.path.isfile(val):
        #     val = os.path.dirname(val)
        return val

    def _make_folder_button(self, label, folder_assigner, x, y, w, h):
        button = QPushButton(label, self)
        button.setGeometry(x, y, w, h)
        dialog = self._get_folder__closure(folder_assigner)
        button.clicked.connect(dialog)

    def _make_submit_button(self, label, x, y, w, h):
        button = QPushButton(label, self)
        button.setGeometry(x, y, w, h)
        button.clicked.connect(self._process_images)

    def _make_exe_labels(self):
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

    def _process_images(self):
        t1 = datetime.datetime.now()
        print(self.source_folder, self.destination_folder)

        files_cr2 = [os.path.join(self.source_folder, f) for f in os.listdir(self.source_folder) if
                     f.lower().endswith('.cr2')]

        [copy2(f, self.destination_folder) for f in files_cr2]

        files_cr2 = [os.path.join(self.destination_folder, f) for f in os.listdir(self.destination_folder) if
                     f.lower().endswith('.cr2')]

        chunk_size = multiprocessing.cpu_count() - 1
        processes = []
        for file in files_cr2:
            p = Popen(args=[self.cr2hdr_path, file], stdout=PIPE)
            processes.append(p)
            processes = _wait(processes, chunk_size)

        _wait(processes, -1)

        files_dng = [os.path.join(self.destination_folder, f) for f in os.listdir(self.destination_folder)
                     if f.lower().endswith('.dng')]

        processes = []
        for file in files_cr2:
            file, ext = os.path.splitext(file)
            if file + '.DNG' in files_dng:
                p = Popen(args=[self.dng_converter_path, '-c', file + '.dng'], stdout=PIPE)
            else:
                p = Popen(args=[self.dng_converter_path, '-c', file + ext], stdout=PIPE)
            processes.append(p)
            processes = _wait(processes, chunk_size)

        for file in files_dng:
            file_name, ext = os.path.splitext(file)
            os.remove(file_name + '.DNG')
            os.rename(file[:-4] + '_1.dng', file[:-4] + '.dng')

        [os.remove(f) for f in files_cr2]

        print('Finished:', datetime.datetime.now(), t1 - datetime.datetime.now())


app = QApplication(sys.argv)
window = Window()
window.show()

# label = QLabel("<font color=red size=40>Hello World!</font>")

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
