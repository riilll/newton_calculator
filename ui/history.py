from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame,
    QScrollArea
)
from PySide6.QtCore import Signal


class HistoryPage(QWidget):

    # Signal ketika pengguna memilih riwayat
    result_selected = Signal(int)

    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)

        title = QLabel("Riwayat Perhitungan")
        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #E8EEFF;
        """)

        subtitle = QLabel(
            "Lihat kembali hasil perhitungan "
            "Newton-Raphson sebelumnya."
        )
        subtitle.setStyleSheet(
            "font-size: 15px; color: #A9B5D0;"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
