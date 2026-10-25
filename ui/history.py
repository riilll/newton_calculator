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

# ===== AREA SCROLL RIWAYAT =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
        """)

        self.container = QWidget()
        self.history_layout = QVBoxLayout(self.container)
        self.history_layout.setSpacing(15)
        self.history_layout.setContentsMargins(0, 10, 10, 10)

        self.history_layout.addStretch()

        scroll.setWidget(self.container)
        layout.addWidget(scroll)

    def update_history(self, history):

# Hapus daftar sebelumnya
        while self.history_layout.count():
            item = self.history_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        if not history:
            empty = QLabel("Belum ada riwayat perhitungan.")
            empty.setStyleSheet(
                "color: #91A1C3; font-size: 16px;"
            )
            self.history_layout.addWidget(empty)

        # Tampilkan riwayat terbaru terlebih dahulu
        for index in reversed(range(len(history))):
            result = history[index]

            card = QFrame()
            card.setStyleSheet("""
                QFrame {
                    background-color: #1B2949;
                    border-radius: 15px;
                }
            """)

            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(25, 20, 25, 20)

            info_layout = QVBoxLayout()

            function_label = QLabel(
                f"f(x) = {result['fungsi']}"
            )
            function_label.setStyleSheet("""
                color: #E8EEFF;
                font-size: 18px;
                font-weight: bold;
            """)

            akar_label = QLabel(
                f"Akar: {result['akar']:.6f}"
            )
            akar_label.setStyleSheet(
                "color: #42D7D0; font-size: 16px;"
            )

            iterasi_solusi = result.get("iterasi_solusi")

            if iterasi_solusi is not None:
                status_text = (
                    f"Solusi ditemukan pada iterasi "
                    f"ke-{iterasi_solusi + 1}"
                )
            else:
                status_text = "Belum konvergen"

            status_label = QLabel(status_text)
            status_label.setStyleSheet(
                "color: #A9B5D0; font-size: 13px;"
            )

info_layout.addWidget(function_label)
            info_layout.addWidget(akar_label)
            info_layout.addWidget(status_label)

            btn_open = QPushButton("Lihat Hasil →")
            btn_open.setFixedSize(150, 45)
            btn_open.setStyleSheet("""
                QPushButton {
                    background-color: #21445E;
                    color: #42D7D0;
                    border-radius: 10px;
                    text-align: center;
                }

                QPushButton:hover {
                    background-color: #305C75;
                }
            """)
