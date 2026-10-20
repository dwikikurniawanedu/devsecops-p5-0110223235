# Catatan Kas Harian

Catatan Kas Harian adalah aplikasi sederhana berbasis Python untuk mencatat pemasukan dan pengeluaran. Aplikasi ini dapat menampilkan daftar transaksi, menghitung saldo, membuat laporan bulanan, dan mengekspor data ke CSV. Data transaksi disimpan secara lokal menggunakan format JSON.

Proyek ini digunakan untuk tugas DevSecOps Pertemuan 5, yaitu menerapkan pengujian otomatis dan pemeriksaan keamanan kode melalui GitHub Actions.

## Teknologi yang Digunakan

- Python 3.12
- Pytest dan pytest-cov untuk pengujian
- Bandit, CodeQL, dan SonarQube untuk analisis keamanan kode
- GitHub Actions untuk menjalankan pipeline CI/CD

## Struktur Proyek

```text
app/                  # Source code aplikasi
tests/                # Unit test
.github/workflows/     # Workflow GitHub Actions
requirements-dev.txt  # Dependencies
sonar-project.properties
README.md
```

Folder `app` berisi enam modul utama, yaitu `main.py`, `models.py`, `transaksi.py`, `validasi.py`, `penyimpanan.py`, dan `laporan.py`.

## Cara Menjalankan

Pastikan Python sudah terinstal. Buka terminal pada folder proyek, kemudian jalankan:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

Contoh penggunaan aplikasi:

```bash
python -m app.main tambah masuk 100000 "Uang saku"
python -m app.main tambah keluar 25000 "Makan siang"
python -m app.main daftar
python -m app.main laporan
```

Untuk menjalankan unit test dan pemeriksaan keamanan:

```bash
python -m pytest -v --cov=app
python -m bandit -r app -ll -ii
```

## Pipeline DevSecOps

Pipeline dibuat menggunakan GitHub Actions melalui file `.github/workflows/devsecops.yml`. Workflow berjalan otomatis ketika terdapat push atau pull request ke branch `main`.

Pipeline terdiri dari dua job:

1. **build:** Menginstal dependencies, memeriksa kode Python, menjalankan unit test, dan menghitung coverage.
2. **sast-scan:** Menjalankan pemeriksaan keamanan menggunakan Bandit, CodeQL, dan SonarQube setelah job build berhasil.

Kedua job menggunakan runner `ubuntu-latest`. Pipeline akan dinyatakan gagal apabila pengujian tidak lulus atau hasil pemeriksaan tidak memenuhi Quality Gate.

Hasil pipeline dapat dilihat melalui tab **Actions** pada repository GitHub.
