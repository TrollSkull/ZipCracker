from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt

from ui.drop_area import DropArea

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("ZIP Password Recovery")
        self.setMinimumSize(760, 440)

        main = QVBoxLayout(self)
        main.setContentsMargins(24, 24, 24, 24)
        main.setSpacing(20)

        # HEADER
        header = QHBoxLayout()
        header.setSpacing(12)

        icon = QLabel("🔒")
        icon.setFixedSize(40, 40)
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("""
            background-color: #2563eb;
            border-radius: 10px;
            color: white;
            font-size: 20px;
        """)

        titles = QVBoxLayout()
        titles.setSpacing(2)

        title = QLabel("ZIP Password Recovery")
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        subtitle = QLabel("Recover passwords from encrypted ZIP archives")
        subtitle.setStyleSheet("font-size: 13px; color: #6b7280;")

        titles.addWidget(title)
        titles.addWidget(subtitle)

        header.addWidget(icon)
        header.addLayout(titles)
        header.addStretch()

        # CONTAINER
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #1e1e1e;
                border-radius: 10px;
            }
        """)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)

        self.drop_area = DropArea()
        container_layout.addWidget(self.drop_area)

        main.addLayout(header)
        main.addWidget(container)
