import os

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QFileDialog
from PySide6.QtGui import QDragEnterEvent, QDropEvent
from PySide6.QtCore import Qt

from core.utils import ALLOWED_EXTENSIONS
from core.utils import format_bytes

class DropArea(QFrame):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setFixedHeight(260)

        self.setObjectName("dropArea")
        self.setStyleSheet("""
            QFrame#dropArea {
                border: 1.5px dashed #6b7280;
                border-radius: 12px;
                background-color: #1e1e1e
            }
        """)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(10)

        self.reset_view()

    def reset_view(self):
        self.clear_layout()

        icon = QLabel("⬆")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 32px; color: #9ca3af;")

        title = QLabel("Drag and drop your encrypted archive here")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 15px;
            font-weight: 500;
            color: #fafafa;
            background-color: #1e1e1e
        """)

        subtitle = QLabel("or click to browse")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 13px; color: #6b7280;")

        support = QLabel("Supports .zip, .rar, and .7z files")
        support.setAlignment(Qt.AlignCenter)
        support.setStyleSheet("font-size: 11px; color: #9ca3af;")

        self.layout.addWidget(icon)
        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)
        self.layout.addSpacing(6)
        self.layout.addWidget(support)

        self.mousePressEvent = self.open_file_dialog

    def show_file(self, file_path: str):
        self.clear_layout()

        file_name = os.path.basename(file_path)
        file_size_bytes = os.path.getsize(file_path)
        file_size = format_bytes(file_size_bytes)

        icon = QLabel("📄")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("""
            font-size: 48px;
            color: #16a34a;
        """)

        name_label = QLabel(file_name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet("""
            font-size: 15px;
            font-weight: 500;
            color: #16a34a;
        """)

        size_label = QLabel(file_size)
        size_label.setAlignment(Qt.AlignCenter)
        size_label.setStyleSheet("""
            font-size: 13px;
            color: #6b7280;
        """)

        change = QLabel("Change file")
        change.setAlignment(Qt.AlignCenter)
        change.setStyleSheet("""
            font-size: 13px;
            color: #2563eb;
        """)

        change.setCursor(Qt.PointingHandCursor)
        change.mousePressEvent = self.open_file_dialog

        self.layout.addWidget(icon)
        self.layout.addWidget(name_label)
        self.layout.addWidget(size_label)
        self.layout.addSpacing(10)
        self.layout.addWidget(change)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

    def is_valid_file(self, path: str) -> bool:
        return path.lower().endswith(ALLOWED_EXTENSIONS)

    def open_file_dialog(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select encrypted archive",
            "",
            "Archives (*.zip *.rar *.7z)"
        )
        if file_path and self.is_valid_file(file_path):
            self.show_file(file_path)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if self.is_valid_file(path):
                self.show_file(path)
                break