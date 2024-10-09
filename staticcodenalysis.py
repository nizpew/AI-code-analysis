from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit, QFileDialog, QGridLayout, QWidget, QApplication, QCheckBox, QLabel
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import subprocess
import tempfile
import os
import glob

class WorkerThread(QThread):
    result_ready = pyqtSignal(str)
    error_ready = pyqtSignal(str)
    analysis_complete = pyqtSignal(bool)

    def __init__(self, paths, analysis_type):
        super().__init__()
        self.paths = paths
        self.analysis_type = analysis_type

    def run(self):
        full_output = ""
        for path in self.paths:
            if not os.path.isfile(path):
                self.error_ready.emit(f"File not found: {path}")
                continue

            try:
                with open(path, 'r') as file:
                    code = file.read()

                max_block_size = 3000
                blocks = [code[i:i + max_block_size] for i in range(0, len(code), max_block_size)]

                for block in blocks:
                    escaped_block = block.replace("'", "'\\''")
                    
                    tgpt_command = f"printf '{escaped_block}' | tgpt -q 'Explain code for {self.analysis_type}'"
                    tgpt_process = subprocess.Popen(tgpt_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    tgpt_output, tgpt_error = tgpt_process.communicate(timeout=60)

                    if tgpt_output:
                        full_output += tgpt_output + "\n\n"

                    if tgpt_error:
                        full_output += f"Error from tgpt: {tgpt_error}\n\n"

                if "The code itself does not directly contain malicious functionality" in full_output:
                    self.analysis_complete.emit(True)
                else:
                    self.analysis_complete.emit(False)

                self.result_ready.emit(full_output)

            except subprocess.TimeoutExpired:
                self.error_ready.emit("Explanation request timed out. Please try again.")
            except Exception as e:
                self.error_ready.emit(f"An error occurred: {e}")

class CodeAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Code Analyzer")
        self.setGeometry(100, 100, 600, 400)
        self.filepaths = []
        
        # Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        # Botões e checkboxes
        self.summary_checkbox = QCheckBox("Explain/Resume Code")
        self.malicious_checkbox = QCheckBox("Identify Malicious Code")
        self.layout.addWidget(self.summary_checkbox, 0, 0)
        self.layout.addWidget(self.malicious_checkbox, 0, 1)
        
        self.button = QPushButton("Import Code Folder")
        self.button.clicked.connect(self.on_folder_clicked)
        self.layout.addWidget(self.button, 1, 0, 1, 2)

        # Texto para exibir código e resultados
        self.textview = QTextEdit()
        self.layout.addWidget(self.textview, 2, 0, 1, 2)
        
        # Indicadores visuais
        self.result_label = QLabel()
        self.layout.addWidget(self.result_label, 3, 0, 1, 2)

    def on_folder_clicked(self):
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        if dialog.exec_():
            folder_path = dialog.selectedFiles()[0]
            self.filepaths = glob.glob(os.path.join(folder_path, '*'))  # Assumindo que você quer analisar todos os arquivos
            if not self.filepaths:
                self.textview.setText("No Python files found in the selected folder.")
                return

            analysis_type = "summary" if self.summary_checkbox.isChecked() else "malicious" if self.malicious_checkbox.isChecked() else "summary"
            self.thread = WorkerThread(self.filepaths, analysis_type)
            self.thread.result_ready.connect(self.update_textview)
            self.thread.error_ready.connect(self.show_error)
            self.thread.analysis_complete.connect(self.update_indicator)
            self.thread.start()

    def update_textview(self, output):
        QTimer.singleShot(0, lambda: self.textview.setText(output))

    def show_error(self, error_message):
        QTimer.singleShot(0, lambda: self.textview.setText(error_message))

    def update_indicator(self, is_safe):
        if is_safe:
            self.result_label.setText("Code is safe.")
            self.result_label.setStyleSheet("color: green;")
        else:
            self.result_label.setText("Code contains potential malicious content.")
            self.result_label.setStyleSheet("color: red;")

if __name__ == "__main__":
    app = QApplication([])
    win = CodeAnalyzer()
    win.show()
    app.exec_()

