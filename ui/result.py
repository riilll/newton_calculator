import numpy as np
import sympy as sp

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView,
    QPushButton, QAbstractItemView
)
from PySide6.QtCore import Qt


class ResultPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def update_result(self, result):
        # ===== AMBIL DATA =====
        akar = result["akar"]
        iterasi = result["iterasi"]
        jumlah = result["jumlah_iterasi"]
        galat = result["galat_akhir"]
        konvergen = result["konvergen"]

        # ===== UPDATE KARTU HASIL =====
        self.root_value[1].setText(f"{akar:.6f}")

        iterasi_solusi = result.get("iterasi_solusi")

        if iterasi_solusi is not None:
            self.iteration_value[1].setText(
                f"Iterasi ke-{iterasi_solusi + 1}"
            )
        else:
            self.iteration_value[1].setText("Belum ditemukan")
        
        self.error_value[1].setText(f"{galat:.8f}")

        # ===== JUMLAH BARIS TABEL =====
        self.table.setRowCount(len(iterasi))

        for row, data in enumerate(iterasi):

            # ===== TENTUKAN STATUS =====
            if data["solusi"]:
                status = "✓ Solusi"
                background = QColor("#174D4A")
                foreground = QColor("#55E6D5")

            elif row == len(iterasi) - 1 and not konvergen:
                status = "Belum Konvergen"
                background = QColor("#594322")
                foreground = QColor("#FFD27A")

            else:
                status = "Proses"
                background = QColor("#050B26")
                foreground = QColor("#E8EEFF")

            # ===== DATA SETIAP KOLOM =====
            values = [
                str(data["n"]),
                f'{data["x"]:.6f}',
                f'{data["fx"]:.6f}',
                f'{data["dfx"]:.6f}',
                f'{data["x_baru"]:.6f}',
                f'{data["galat"]:.6f}',
                status
            ]

            # ===== MASUKKAN DATA KE TABEL =====
            for col, value in enumerate(values):
                item = QTableWidgetItem(value)

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                item.setBackground(QBrush(background))
                item.setForeground(QBrush(foreground))

                self.table.setItem(row, col, item)

            self.table.setRowHeight(row, 48)
            # Perbarui grafik berdasarkan hasil perhitungan
            self.update_graph(result)

        # Reset tabel ke tampilan ringkas
        self.expanded = False
        self.adjust_table_height()

        # Perbarui grafik
        self.update_graph(result)
