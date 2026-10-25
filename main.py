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
