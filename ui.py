import datetime
import multiprocessing
import os
from shutil import copy2
from subprocess import Popen, PIPE
import sys
import time

from PySide2.QtCore import Qt, QSettings
from PySide2.QtWidgets import QApplication, QFileDialog, QPushButton, QLabel, QWidget, QTextEdit


def _wait(processes, chunk_size):
    while True:
        processes = [p for p in processes if p.poll() is None]
        if len(processes) >= chunk_size and processes:
            time.sleep(1)
        else:
            break

    return processes


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.default_converter_path_name = 'adobe_dng_converter_path'
        self.default_source_folder_name = 'source_folder'
        self.default_destination_folder_name = 'destination_folder'

        self.default_values = QSettings('Brilliant Imagery', 'CR2 Processor')

        self.dng_converter_path = self.default_values.value(self.default_converter_path_name)
        self.source_folder = self.default_values.value(self.default_source_folder_name)
        self.destination_folder = self.default_values.value(self.default_destination_folder_name)
        self.cr2hdr_path = os.path.join(resource_path(''), 'cr2hdr.exe')

        self.setWindowTitle("DNG Converter")
        self.setGeometry(600, 300, 600, 300)

        self._make_file_button('Adobe DNG Converter', lambda v: setattr(self, 'dng_converter_path', v),
                               self.default_converter_path_name,
                               lambda: self.dng_converter_path, 10, 20, 300, 150, 30)
        self._make_folder_button('Source Folder', lambda v: setattr(self, 'source_folder', v),
                                 self.default_source_folder_name,
                                 lambda: self.source_folder, 10, 50, 300, 150, 30)
        self._make_folder_button('Destination Folder', lambda v: setattr(self, 'destination_folder', v),
                                 self.default_destination_folder_name,
                                 lambda: self.destination_folder, 10, 80, 300, 150, 30)
        self._make_submit_button('Process!!!', 10, 150, 100, 30)

    def _get_file__closure(self, assigner, default_value_name):
        reference_file = self.default_values.value(default_value_name)

        def get_file():
            file = QFileDialog.getOpenFileName(self, file=reference_file)[0]
            assigner(file)

        return get_file

    def _get_folder__closure(self, assigner, default_value_name):
        reference_folder = self.default_values.value(default_value_name)

        def get_folder():
            folder = QFileDialog.getExistingDirectory(self, dir=reference_folder)
            assigner(folder)

        return get_folder

    def _make_file_button(self, label, file_assigner, default_value_name, target_path, x, y, tw, bw, h):
        default_value = self.default_values.value(default_value_name)
        dialog = self._get_file__closure(file_assigner, default_value)

        self._make_textbox_and_button(label, dialog, default_value, target_path, x, y, tw, bw, h)

    def _make_folder_button(self, label, folder_assigner, default_value_name, target_path, x, y, tw, bw, h):
        default_value = self.default_values.value(default_value_name)
        dialog = self._get_folder__closure(folder_assigner, default_value)
        self._make_textbox_and_button(label, dialog, default_value, target_path, x, y, tw, bw, h)

    def _make_textbox_and_button(self, label, dialog, path, target_path, x, y, tw, bw, h):
        if not path:
            path = ''
        button = QPushButton(label, self)
        button.setGeometry(tw + x, y, bw, h)
        button.clicked.connect(dialog)
        textbox = QTextEdit(path, self)
        textbox.setGeometry(x, y, tw, h)
        button.clicked.connect(lambda: textbox.setText(target_path()))

    def _make_submit_button(self, label, x, y, w, h):
        button = QPushButton(label, self)
        button.setGeometry(x, y, w, h)
        button.clicked.connect(self._process_images)

    def _process_images(self):
        t1 = datetime.datetime.now()
        print(self.source_folder, self.destination_folder)
        self.default_values.setValue(self.default_converter_path_name, self.dng_converter_path)
        self.default_values.setValue(self.default_source_folder_name, self.source_folder)
        self.default_values.setValue(self.default_destination_folder_name, self.destination_folder)

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

app.exec_()
sys.exit(0)
