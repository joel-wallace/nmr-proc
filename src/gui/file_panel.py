from PySide6.QtWidgets import (
    QWidget, QTreeView, QFileSystemModel,
    QDir
        )

class FilePanel(QWidget):
    def __init__(self):
        super.__init__()
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

        ## Need getters and setters for dir path etc