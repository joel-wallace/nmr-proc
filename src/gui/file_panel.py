from PySide6.QtWidgets import (
    QWidget, QTreeView, QFileSystemModel,
    QVBoxLayout, QPushButton, QLineEdit, 
    QFileDialog
        )

from PySide6.QtCore import QDir

class FilePanel(QWidget):
    def __init__(self):
        super().__init__()
        # Open directory button connected to select_directory function
        # QLineEdit with current directory, non-editable but copy-pastable
        self.tree = QTreeView()
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        self.tree.hideColumn(1)
        self.tree.hideColumn(2)
        self.tree.hideColumn(3)

        self.open_button = QPushButton("Select Directory")
        self.open_button.clicked.connect(self.select_directory)

        self.path_edit = QLineEdit("No directory selected")
        self.path_edit.setReadOnly(True)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.open_button)
        self.layout.addWidget(self.path_edit)
        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)

    def get_dir_path(self):
        return self.path_edit.text
    
    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.model.setRootPath(directory)
            self.tree.setRootIndex(self.model.index(directory))
            self.path_edit.setText(directory)