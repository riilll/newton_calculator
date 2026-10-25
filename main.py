from PySide6.QtGui import QFontDatabase, QFont
from pathlib import Path
import math
from ui.history import HistoryPage
from sympy import (
    symbols,
    lambdify,
    diff,
    simplify,
    SympifyError
)
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)

from PySide6.QtWidgets import QMessageBox, QStackedWidget,QScrollArea
from ui.result import ResultPage

from logic.newton import newton_raphson

import sys

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit, 
    QGridLayout, 
    QSizePolicy
)
from PySide6.QtCore import Qt

class NewtonApp(QWidget):
    def __init__(self):
        super().__init__()
        self.history_data = []

        self.setWindowTitle("Metode Newton - Kelompok 3")
        self.resize(1200, 850)
        self.setMinimumSize(900, 650)

        self.setStyleSheet("""
            QWidget {
                background-color: #050B26;
                color: #E8EEFF;
                font-family: 'Poppins';
            }

            QFrame#header {
                background-color: #1C2D56;
            }

            QFrame#sidebar {
                background-color: #1B2949;
                border-radius: 20px;
            }

            QPushButton {
                background: transparent;
                border: none;
                color: #A9B5D0;
                text-align: left;
                padding: 16px;
                border-radius: 14px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #263A5B;
            }

            QPushButton#active {
                background-color: #21445E;
                color: #49D8D1;
            }

            QFrame#formula {
                background-color: #1B2949;
                border-radius: 18px;
            }

            QFrame#inputCard {
                background-color: #1B2949;
                border: 1px solid #2B3C60;
                border-radius: 18px;
            }

            QLabel#inputLabel {
                color: #91A1C3;
                font-size: 15px;
                background: transparent;
            }

            QLineEdit {
                background: transparent;
                color: #E8EEFF;
                border: none;
                font-size: 20px;
                padding: 0px;
                selection-background-color: #42D7D0;
            }

            QLineEdit::placeholder {
                color: #7889A8;
            }

            QPushButton#calculate {
                background-color: #39BEDD;
                color: #06142E;
                font-size: 21px;
                border-radius: 15px;
                text-align: center;
            }

            QPushButton#calculate:hover {
                background-color: #55D8E5;
            }

            QPushButton#reset {
                background-color: #1B2949;
                color: #A9B5D0;
                border: 1px solid #2B3C60;
                font-size: 20px;
                border-radius: 15px;
                text-align: center;
            }
        """)

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

# ===== HEADER =====
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(95)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(25, 0, 40, 0)

        logo = QLabel("◆")
        logo.setStyleSheet(
            "color: #42D7D0; font-size: 35px;"
            "background: transparent;"
        )

        title = QLabel("Metode Newton")
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold;"
            "background: transparent;"
        )

        author = QLabel("By Kelompok 3")
        author.setStyleSheet(
            "font-size: 18px; color: #91A1C3;"
            "background: transparent;"
        )

        header_layout.addWidget(logo)
        header_layout.addSpacing(12)
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(author)

        main_layout.addWidget(header)

        # ===== BODY =====
        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(25, 25, 25, 25)
        body_layout.setSpacing(35)

        # ===== SIDEBAR =====
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 20)
        sidebar_layout.setSpacing(12)

        workspace = QLabel("WORKSPACE")
        workspace.setStyleSheet(
            "color: #91A1C3; font-size: 17px;"
            "background: transparent;"
        )

        sidebar_layout.addWidget(workspace)

        self.btn_calculator = QPushButton("●  Kalkulator")
        self.btn_calculator.setObjectName("active")

        self.btn_result = QPushButton("●  Hasil")
        self.btn_history = QPushButton("●  Riwayat")

        sidebar_layout.addWidget(self.btn_calculator)
        sidebar_layout.addWidget(self.btn_result)
        sidebar_layout.addWidget(self.btn_history)

        sidebar_layout.addStretch()

        method = QLabel("METODE\nNewton-Raphson")
        method.setStyleSheet("""
            background-color: #111A35;
            border: 1px solid #304061;
            border-radius: 12px;
            padding: 15px;
            font-size: 14px;
        """)

        sidebar_layout.addWidget(method)
        body_layout.addWidget(sidebar)

        # ===== MAIN CONTENT =====
        self.pages = QStackedWidget()

        # Halaman kalkulator
        calculator_page = QWidget()

        content_layout = QVBoxLayout(calculator_page)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)

        heading = QLabel("Cari akar persamaan")
        heading.setStyleSheet(
            "font-size: 30px; font-weight: bold;"
        )

        subtitle = QLabel(
            "Masukkan fungsi, turunan, dan tebakan awal "
            "untuk memulai iterasi."
        )
        subtitle.setStyleSheet(
            "font-size: 16px; color: #A9B5D0;"
        )

        content_layout.addWidget(heading)
        content_layout.addWidget(subtitle)

        # ===== FORMULA CARD =====
        formula_card = QFrame()
        formula_card.setObjectName("formula")
        formula_card.setFixedHeight(140)

        formula_layout = QVBoxLayout(formula_card)
        formula_layout.setContentsMargins(28, 20, 28, 20)

        formula_label = QLabel("RUMUS ITERASI")
        formula_label.setStyleSheet(
            "color: #91A1C3; font-size: 16px;"
            "background: transparent;"
        )

        formula_text = QLabel("xₙ₊₁ = xₙ − f(xₙ) / f′(xₙ)")
        formula_text.setStyleSheet(
            "font-size: 35px; font-weight: bold;"
            "background: transparent;"
        )

        formula_layout.addWidget(formula_label)
        formula_layout.addWidget(formula_text)

        content_layout.addSpacing(10)
        
        content_layout.addWidget(formula_card)
        content_layout.addSpacing(20)

        # ===== INPUT BARIS PERTAMA =====
        row1 = QHBoxLayout()
        row1.setSpacing(20)

        function_card, self.input_function = (
            self.create_input_card(
                "FUNGSI f(x)", "x^3 - 2*x - 5"
            )
        )

        derivative_card, self.input_derivative = (
            self.create_input_card(
                "TURUNAN f'(x)", "3*x^2 - 2"
            )
        )
        self.input_derivative.setReadOnly(True)
        self.input_derivative.setPlaceholderText("Terisi otomatis dari f(x)")

        self.input_function.textChanged.connect(
            self.update_derivative
        )

        row1.addWidget(function_card)
        row1.addWidget(derivative_card)

        content_layout.addLayout(row1)
        content_layout.addSpacing(10)

        # ===== INPUT BARIS KEDUA =====
        row2 = QHBoxLayout()
        row2.setSpacing(20)

        initial_card, self.input_initial = (
            self.create_input_card("TEBAKAN AWAL (x₀)", "2")
        )

        tolerance_card, self.input_tolerance = (
            self.create_input_card("TOLERANSI", "0.0001")
        )

        iteration_card, self.input_iteration = (
            self.create_input_card("ITERASI MAKSIMUM", "20")
        )

        row2.addWidget(initial_card)
        row2.addWidget(tolerance_card)
        row2.addWidget(iteration_card)

        content_layout.addLayout(row2)
        content_layout.addSpacing(20)

        # ===== TOMBOL =====
        button_layout = QHBoxLayout()
        button_layout.setSpacing(18)

        self.btn_calculate = QPushButton("Hitung Akar  ↗")
        self.btn_calculate.setObjectName("calculate")
        self.btn_calculate.setFixedSize(260, 60)

        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setObjectName("reset")
        self.btn_reset.setFixedSize(160, 60)

        button_layout.addWidget(self.btn_calculate)
        button_layout.addWidget(self.btn_reset)
        button_layout.addStretch()

        content_layout.addLayout(button_layout)

        content_layout.addStretch()

        # ===== HALAMAN HASIL =====
        self.result_page = ResultPage()

        result_scroll = QScrollArea()
        result_scroll.setWidgetResizable(True)
        result_scroll.setFrameShape(QFrame.Shape.NoFrame)
        result_scroll.setWidget(self.result_page)

        result_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #050B26;
                border: none;
            }
        """)

        # Masukkan kedua halaman
        self.pages.addWidget(calculator_page)
        self.pages.addWidget(result_scroll)
        self.history_page = HistoryPage()
        self.pages.addWidget(self.history_page)

        # Tampilkan kalkulator pertama kali
        self.pages.setCurrentIndex(0)

        body_layout.addWidget(self.pages, 1)
        main_layout.addLayout(body_layout, 1)

                # ===== NAVIGASI =====
        self.btn_calculator.clicked.connect(self.show_calculator)
        self.btn_result.clicked.connect(self.show_result)
        self.result_page.btn_again.clicked.connect(self.show_calculator)
        self.btn_history.clicked.connect(self.show_history)
        self.history_page.result_selected.connect(
            self.open_history_result
        )


    def create_input_card(self, label_text, default_value):
        card = QFrame()
        card.setObjectName("inputCard")
        card.setMinimumHeight(115)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 15, 25, 15)
        layout.setSpacing(10)

        label = QLabel(label_text)
        label.setObjectName("inputLabel")

        input_field = QLineEdit()
        input_field.setPlaceholderText(default_value)

        layout.addWidget(label)
        layout.addWidget(input_field)

        return card, input_field

    
    def reset_inputs(self):
        self.input_function.clear()
        self.input_derivative.clear()
        self.input_initial.clear()
        self.input_tolerance.clear()
        self.input_iteration.clear()

    def show_calculator(self):
        self.pages.setCurrentIndex(0)
        self.set_active_menu(self.btn_calculator)

    def show_result(self):
        self.pages.setCurrentIndex(1)
        self.set_active_menu(self.btn_result)

    def set_active_menu(self, active_button):
        buttons = [
            self.btn_calculator,
            self.btn_result,
            self.btn_history
        ]

        for button in buttons:
            if button == active_button:
                button.setObjectName("active")
            else:
                button.setObjectName("")

            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def update_derivative(self):
        fungsi_teks = self.input_function.text().strip()

        # Kalau input kosong, kosongkan turunannya
        if not fungsi_teks:
            self.input_derivative.clear()
            return

        try:
            x = sp.symbols("x")

            transformations = (
                standard_transformations
                + (
                    implicit_multiplication_application,
                    convert_xor
                )
            )

            # Ubah teks menjadi ekspresi matematika
            fungsi = parse_expr(
                fungsi_teks,
                transformations=transformations,
                local_dict={
                    "x": x,
                    "sin": sp.sin,
                    "cos": sp.cos,
                    "tan": sp.tan,
                    "exp": sp.exp,
                    "log": sp.log,
                    "sqrt": sp.sqrt
                }
            )

            # Hitung turunan otomatis
            turunan = sp.diff(fungsi, x)

            # Tampilkan dalam format yang mudah dibaca
            turunan_teks = str(turunan).replace("**", "^")

            self.input_derivative.setText(turunan_teks)

        except (Exception):
            # Ketika pengguna masih mengetik
            # ekspresi yang belum lengkap
            self.input_derivative.clear()

    def calculate_root(self):
        try:
            # 1. Ambil teks dari kolom input
            fungsi_teks = self.input_function.text().strip()
            turunan_teks = self.input_derivative.text().strip()
            if not fungsi_teks:
                QMessageBox.warning(
                    self,
                    "Input Kosong",
                    "Silakan masukkan fungsi f(x) terlebih dahulu."
                )
                return

            if not turunan_teks:
                QMessageBox.warning(
                    self,
                    "Fungsi Tidak Valid",
                    "Turunan otomatis belum berhasil dihitung. "
                    "Periksa kembali penulisan fungsi f(x)."
                )
                return

            x0 = float(self.input_initial.text())
            toleransi = float(self.input_tolerance.text())
            max_iterasi = int(self.input_iteration.text())

            # 2. Validasi parameter
            if not fungsi_teks or not turunan_teks:
                raise ValueError(
                    "Fungsi dan turunan tidak boleh kosong."
                )

            if not math.isfinite(x0):
                raise ValueError(
                    "Tebakan awal harus berupa angka terbatas."
                )

            if not math.isfinite(toleransi) or toleransi <= 0:
                raise ValueError(
                    "Toleransi harus lebih besar dari nol."
                )

            if not 1 <= max_iterasi <= 1000:
                raise ValueError(
                    "Iterasi maksimum harus antara 1 dan 1000."
                )

            # 3. Membaca ekspresi matematika
            x = symbols("x")

            transformations = (
                standard_transformations
                + (implicit_multiplication_application, convert_xor)
            )

            allowed_names = {
                "x": x,
                "sin": __import__("sympy").sin,
                "cos": __import__("sympy").cos,
                "tan": __import__("sympy").tan,
                "exp": __import__("sympy").exp,
                "log": __import__("sympy").log,
                "sqrt": __import__("sympy").sqrt,
            }

            # Gunakan hanya pada ekspresi yang dipercaya.
            # parse_expr tidak aman untuk input sembarang pengguna.
            fungsi_expr = parse_expr(
                fungsi_teks,
                local_dict=allowed_names,
                transformations=transformations
            )

            turunan_expr = parse_expr(
                turunan_teks,
                local_dict=allowed_names,
                transformations=transformations
            )

            # 4. Periksa variabel dan turunan
            if not fungsi_expr.free_symbols <= {x}:
                raise ValueError(
                    "Fungsi hanya boleh menggunakan variabel x."
                )

            if not turunan_expr.free_symbols <= {x}:
                raise ValueError(
                    "Turunan hanya boleh menggunakan variabel x."
                )

            turunan_asli = diff(fungsi_expr, x)

            if simplify(turunan_asli - turunan_expr) != 0:
                raise ValueError(
                    "Turunan tidak sesuai dengan fungsi f(x)."
                )

            # 5. Ubah ekspresi menjadi fungsi numerik
            f = lambdify(x, fungsi_expr, modules="math")
            df = lambdify(x, turunan_expr, modules="math")

            # 6. Jalankan Newton-Raphson
            akar, iterasi, iterasi_solusi = newton_raphson(
                f,
                df,
                x0,
                toleransi,
                max_iterasi
            )

            if not math.isfinite(akar):
                raise ValueError(
                    "Perhitungan menghasilkan nilai tidak valid."
                )

            jumlah_iterasi = len(iterasi)

            if iterasi_solusi is not None:
                galat_akhir = iterasi[iterasi_solusi]["galat"]
            else:
                galat_akhir = iterasi[-1]["galat"]

            # 7. Simpan hasil untuk halaman berikutnya
            self.last_result = {
                "fungsi": fungsi_teks,
                "turunan": turunan_teks,
                "akar": akar,
                "jumlah_iterasi": jumlah_iterasi,
                "galat_akhir": galat_akhir,
                "iterasi": iterasi,
                "iterasi_solusi": iterasi_solusi,
                "konvergen": iterasi_solusi is not None
            }
        except (
            ValueError,
            ZeroDivisionError,
            OverflowError,
            TypeError,
            SympifyError,
            SyntaxError
        ) as error:
            QMessageBox.warning(
                self,
                "Kesalahan Perhitungan",
                str(error)
            )







if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ===== LOAD FONT POPPINS =====
    font_folder = Path(__file__).resolve().parent / "assets" / "fonts"

    for font_file in font_folder.glob("*.ttf"):
        QFontDatabase.addApplicationFont(str(font_file))

    app.setFont(QFont("Poppins", 10))

    window = NewtonApp()
    window.show()

    sys.exit(app.exec())
