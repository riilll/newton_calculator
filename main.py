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
