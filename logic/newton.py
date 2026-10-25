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

        # Tandai solusi pertama yang memenuhi toleransi
        solusi = galat < toleransi and akar_solusi is None

        if solusi:
            akar_solusi = x_baru
            iterasi_solusi = n

        hasil_iterasi.append({
            "n": n,
            "x": x,
            "fx": fx,
            "dfx": dfx,
            "x_baru": x_baru,
            "galat": galat,
            "solusi": solusi
        })

        x = x_baru

    # Jika belum ditemukan solusi, gunakan pendekatan terakhir
    if akar_solusi is None:
        akar_solusi = x

    return akar_solusi, hasil_iterasi, iterasi_solusi
