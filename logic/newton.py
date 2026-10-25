import math

def newton_raphson(f, df, x0, toleransi, max_iterasi):
    hasil_iterasi = []
    x = x0

    akar_solusi = None
    iterasi_solusi = None

    for n in range(max_iterasi):
        fx = f(x)
        dfx = df(x)

        if not all(math.isfinite(v) for v in (x, fx, dfx)):
            raise ValueError("Perhitungan menghasilkan nilai tidak valid.")

        if abs(dfx) < 1e-12:
            raise ValueError("Turunan terlalu dekat dengan nol.")

        x_baru = x - fx / dfx
        galat = abs(x_baru - x)

        if not math.isfinite(x_baru):
            raise ValueError("Hasil iterasi tidak valid.")

        x = x_baru
