import math

def newton_raphson(f, df, x0, toleransi, max_iterasi):
    hasil_iterasi = []
    x = x0

    akar_solusi = None
    iterasi_solusi = None
