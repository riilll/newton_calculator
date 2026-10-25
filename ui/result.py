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

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        # ===== JUDUL =====
        title = QLabel("Hasil Pendekatan Akar")
        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #E8EEFF;
        """)

        subtitle = QLabel(
            "Hasil perhitungan berdasarkan fungsi, "
            "turunan, dan tebakan awal yang diinput."
        )
        subtitle.setStyleSheet(
            "color: #A9B5D0; font-size: 15px;"
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ===== KARTU HASIL =====
        result_card = QFrame()
        result_card.setStyleSheet("""
            QFrame {
                background-color: #21405A;
                border-radius: 18px;
            }
        """)
        result_card.setMinimumHeight(125)

        card_layout = QHBoxLayout(result_card)
        card_layout.setContentsMargins(25, 20, 25, 20)

        self.root_value = self.create_result_value(
            "Akar Hampiran", "0.0000"
        )

        self.iteration_value = self.create_result_value(
            "Solusi Ditemukan", "-"
        )

        self.error_value = self.create_result_value(
            "Galat Akhir", "0.0000"
        )

        card_layout.addLayout(self.root_value[0])
        card_layout.addLayout(self.iteration_value[0])
        card_layout.addLayout(self.error_value[0])

        layout.addWidget(result_card)

        # ===== JUDUL TABEL =====
        table_title = QLabel("Tabel Iterasi")
        table_title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #E8EEFF;
        """)

        formula = QLabel(
            "xₙ₊₁ = xₙ − f(xₙ) / f′(xₙ)"
        )
        formula.setStyleSheet(
            "color: #A9B5D0; font-size: 13px;"
        )

        layout.addWidget(table_title)
        layout.addWidget(formula)

        # ===== TABEL ITERASI =====
        self.table = QTableWidget()
        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels([
            "n", "xₙ", "f(xₙ)",
            "f′(xₙ)", "xₙ₊₁", "Galat", "Status"
        ])

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setMinimumHeight(260)

        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #050B26;
                color: #E8EEFF;
                border: none;
                gridline-color: transparent;
                font-size: 14px;
            }

            QHeaderView::section {
                background-color: #1B2949;
                color: #A9B5D0;
                border: none;
                padding: 12px;
                font-size: 16px;
            }

            QTableWidget::item {
                padding: 10px;
                border: none;
            }
        """)

        layout.addWidget(self.table)

        # ===== TOMBOL EXPAND TABEL =====
        self.btn_expand = QPushButton("▼ Tampilkan Semua Iterasi")
        self.btn_expand.setFixedHeight(42)

        self.btn_expand.setStyleSheet("""
            QPushButton {
                background-color: #1B2949;
                color: #42D7D0;
                border: 1px solid #304061;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 14px;
                text-align: center;
            }

            QPushButton:hover {
                background-color: #263A5B;
            }
        """)

        layout.addWidget(self.btn_expand)

        self.expanded = False
        self.btn_expand.clicked.connect(self.toggle_table)
                # ===== JUDUL GRAFIK =====
        graph_title = QLabel("Grafik Fungsi")
        graph_title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #E8EEFF;
        """)

        layout.addSpacing(20)
        layout.addWidget(graph_title)

        # ===== GRAFIK =====
        self.graph = self.create_graph()
        self.graph.setMinimumHeight(350)

        layout.addWidget(self.graph)

        # ===== TOMBOL HITUNG LAGI =====
        self.btn_again = QPushButton("Hitung Lagi  ↗")
        self.btn_again.setFixedSize(190, 55)
        self.btn_again.setStyleSheet("""
            QPushButton {
                background-color: #39BEDD;
                color: #06142E;
                border: none;
                border-radius: 13px;
                font-size: 18px;
                text-align: center;
            }

            QPushButton:hover {
                background-color: #55D8E5;
            }
        """)

        layout.addWidget(self.btn_again)
        layout.addStretch()

    def toggle_table(self):
        self.expanded = not self.expanded
        self.adjust_table_height()

    def adjust_table_height(self):
        total_rows = self.table.rowCount()

        if self.expanded:
            visible_rows = total_rows
            self.btn_expand.setText("▲ Sembunyikan Iterasi")
        else:
            visible_rows = min(5, total_rows)
            self.btn_expand.setText(
                f"▼ Tampilkan Semua Iterasi ({total_rows})"
            )

        header_height = self.table.horizontalHeader().height()

        rows_height = sum(
            self.table.rowHeight(row)
            for row in range(visible_rows)
        )

        self.table.setFixedHeight(
            header_height + rows_height + 4
        )

    def create_result_value(self, title, value):
        container = QVBoxLayout()
        container.setSpacing(10)

        label = QLabel(title)
        label.setStyleSheet(
            "color: #42D7D0; font-size: 15px;"
        )

        number = QLabel(value)
        number.setStyleSheet("""
            color: #42D7D0;
            font-size: 32px;
            font-weight: 500;
        """)

        container.addWidget(label)
        container.addWidget(number)

        return container, number

    def create_graph(self):

        # Membuat wadah grafik
        self.figure = Figure(
            figsize=(8, 4),
            facecolor="#1B2949"
        )

        self.canvas = FigureCanvasQTAgg(self.figure)

        # Membuat area koordinat
        self.ax = self.figure.add_subplot(111)

        # Menyesuaikan warna grafik
        self.ax.set_facecolor("#1B2949")

        return self.canvas

    def update_graph(self, result):
        # Mengambil fungsi dan akar
        fungsi_teks = result["fungsi"]
        akar = result["akar"]

        # Membaca fungsi matematika
        x = sp.symbols("x")

        fungsi_expr = sp.sympify(
            fungsi_teks.replace("^", "**")
        )

        f = sp.lambdify(x, fungsi_expr, "numpy")

        # Membuat rentang grafik di sekitar akar
        x_values = np.linspace(
            akar - 3,
            akar + 3,
            500
        )

        y_values = f(x_values)

        # Bersihkan grafik sebelumnya
        self.ax.clear()

        # Warna latar
        self.ax.set_facecolor("#1B2949")

        # Gambar kurva fungsi
        self.ax.plot(
            x_values,
            y_values,
            color="#39C8F4",
            linewidth=3,
            label=f"f(x) = {fungsi_teks}"
        )

        # Garis sumbu X
        self.ax.axhline(
            0,
            color="#91A1C3",
            linewidth=1
        )

        # Garis sumbu Y
        self.ax.axvline(
            0,
            color="#91A1C3",
            linewidth=1
        )

        # Titik akar dengan garis tepi putih
        self.ax.scatter(
            [akar],
            [f(akar)],
            color="#42D7D0",
            edgecolors="white",
            linewidths=2,
            s=110,
            zorder=5
        )

        # Garis vertikal putus-putus
        self.ax.vlines(
            x=akar,
            ymin=self.ax.get_ylim()[0],
            ymax=0,
            colors="#42D7D0",
            linestyles="dashed",
            linewidth=1.5,
            alpha=0.8
        )
        self.ax.annotate(
            f"AKAR DITEMUKAN\nx ≈ {akar:.6f}",
            xy=(akar, f(akar)),
            xytext=(80, -45),
            textcoords="offset points",
            color="#42D7D0",
            fontsize=10,
            fontweight="bold",
            bbox=dict(
                boxstyle="round,pad=0.8",
                facecolor="#10283F",
                edgecolor="#42D7D0",
                linewidth=1
            ),
            arrowprops=dict(
                arrowstyle="-",
                color="#42D7D0",
                linewidth=1
            )
        )
        # Grid
        self.ax.grid(
            True,
            color="#344465",
            alpha=0.5
        )

        # Warna angka pada sumbu
        self.ax.tick_params(
            colors="#A9B5D0"
        )

        # Warna garis tepi
        for spine in self.ax.spines.values():
            spine.set_color("#344465")

        # Legend
        self.ax.legend(
            facecolor="#1B2949",
            labelcolor="white",
            edgecolor="#344465"
        )

        self.figure.tight_layout()

        # Perbarui tampilan
        self.canvas.draw()
