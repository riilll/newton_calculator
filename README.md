# Metode Newton – Kalkulator Newton-Raphson
Aplikasi desktop (GUI) berbasis PySide6 untuk mencari akar persamaan f(x) = 0 menggunakan metode Newton-Raphson.

xₙ₊₁ = xₙ − f(xₙ) / f′(xₙ)

Kelompok 3
Anggota: 
1. Muhammad Fahril Khalifi 
2. Muhammad Reza Nurhakim 
3. Aulia Faradina
4. As-Sajadah Khaira


== Fitur ==
- Turunan otomatis: cukup ketik `f(x)`, kolom `f′(x)` terisi sendiri (memakai SymPy).
- Tabel iterasi: menampilkan `n`, `xₙ`, `f(xₙ)`, `f′(xₙ)`, `xₙ₊₁`, galat, dan status tiap iterasi.
- Grafik fungsi dengan penanda titik akar (Matplotlib).
- Riwayat perhitungan: hasil sebelumnya bisa dibuka kembali.
- Validasi input: toleransi, iterasi maksimum, turunan mendekati nol, nilai tidak valid, dan lainnya.

== Download Library ==
Pastikan Python 3.9+ sudah terpasang, lalu jalankan:
    pip install PySide6 sympy numpy matplotlib

## Cara Menjalankan
Buka terminal di folder proyek, lalu:
    python main.py

## Cara Pakai
1. Isi **f(x)**, contoh `x^3 - 2*x - 5` (turunan terisi otomatis).
2. Isi **tebakan awal** (contoh `2`), **toleransi** (contoh `0.0001`), dan **iterasi maksimum** (contoh `20`).
3. Klik **Hitung Akar**. Hasil, tabel iterasi, dan grafik muncul di halaman Hasil.
4. Menu **Riwayat** untuk melihat perhitungan sebelumnya.
