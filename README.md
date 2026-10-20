# Catatan Kas Harian

Aplikasi terminal sederhana untuk mencatat pemasukan dan pengeluaran kas, melihat saldo, menyaring transaksi bulanan, dan mengekspor data ke CSV. Data disimpan sebagai JSON pada komputer pengguna, sehingga aplikasi tidak memerlukan database server. Proyek ini dipakai untuk tugas DevSecOps Pertemuan 5.

## Fitur utama

- Tambah transaksi pemasukan dan pengeluaran dengan tanggal serta keterangan.
- Validasi nominal, jenis transaksi, tanggal dan keterangan.
- Tampilkan transaksi, hapus transaksi menurut ID dan buat ringkasan kas.
- Filter ringkasan berdasarkan bulan dan ekspor data ke CSV.

## Teknologi

- **Bahasa:** Python 3.12 (tanpa framework web)
- **Pengujian:** pytest, pytest-cov
- **SAST:** Bandit, CodeQL, SonarQube Cloud
- **Otomasi CI:** GitHub Actions dengan runner `ubuntu-latest`
- **Penyimpanan:** file JSON lokal

## Struktur kode

```text
app/
├── __init__.py     # penanda package
├── main.py         # antarmuka command-line
├── models.py       # model data transaksi
├── transaksi.py    # logika tambah, daftar, dan hapus
├── validasi.py     # pemeriksaan input
├── penyimpanan.py  # baca/tulis JSON
└── laporan.py      # saldo, filter bulanan dan CSV
tests/              # pengujian otomatis
.github/workflows/devsecops.yml
```

Enam file `.py` di `app/` berisi kode fungsional; `__init__.py` tidak dihitung sebagai source code fungsional.

## Menjalankan aplikasi

Python minimal versi 3.10. Dari direktori proyek:

**Ubuntu / WSL**

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

**Windows PowerShell**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

Contoh pemakaian (berjalan di kedua lingkungan):

```bash
python -m app.main tambah masuk 100000 "Uang saku"
python -m app.main tambah keluar 25000 "Makan siang"
python -m app.main daftar
python -m app.main laporan
python -m app.main laporan --bulan 2026-10
python -m app.main ekspor data/laporan.csv
python -m app.main hapus 1
```

Transaksi lokal disimpan di `data/transaksi.json`, yang diabaikan Git. Gunakan `--file nama.json` sebelum subcommand jika memerlukan file lain.

## Pengujian lokal

```bash
python -m pytest -q --cov=app --cov-report=term-missing --cov-report=xml:coverage.xml
python -m bandit -r app -ll -ii
```

Parameter Bandit: `-ll` berarti severity minimal MEDIUM; `-ii` berarti confidence minimal MEDIUM.

## Gambaran pipeline DevSecOps

Workflow `.github/workflows/devsecops.yml` berjalan saat **push** ke branch `main` dan **pull_request** dengan target branch `main`.

| Job | Tugas | Aturan lulus / gagal |
|---|---|---|
| `build` | Instal dependensi, cek sintaks Python, jalankan unit test dan menghasilkan `coverage.xml` | Test harus lulus dan coverage minimal 80% |
| `sast-scan` (`needs: build`) | CodeQL, Bandit, SonarQube Cloud | Bandit tidak menemukan isu sesuai ambang; SonarQube Quality Gate harus PASSED |

Kedua job menggunakan `ubuntu-latest`. Hasil CodeQL diunggah melalui `github/codeql-action/analyze` dan dapat diperiksa pada **Security > Code scanning**. Coverage dari job `build` dikirim ke `sast-scan` melalui GitHub Actions artifacts agar dapat digunakan SonarQube.

Pipeline ini berfokus pada **Continuous Integration dan pemeriksaan keamanan**, belum menyertakan deployment otomatis. Jika pemeriksaan gagal, workflow akan merah. Agar kegagalan juga benar-benar **mencegah merge**, tambahkan required status checks pada aturan branch `main` di pengaturan GitHub.

## Pengaturan SonarQube Cloud (perlu dilakukan oleh pemilik repository)

1. Buat repository GitHub **Public**, lalu unggah proyek ke branch `main`.
2. Login dengan akun GitHub ke https://sonarcloud.io. Impor repository dan pilih **CI-based analysis / GitHub Actions**, bukan Automatic Analysis.
3. Catat nilai **Organization Key** dan **Project Key** yang diberikan SonarQube Cloud.
4. Buat analysis token dengan izin proyek yang sesuai. **Jangan menulis token di kode, YAML, atau screenshot.**
5. Buka GitHub **Settings > Secrets and variables > Actions** dan buat:
   - **Secret**: `SONAR_TOKEN`
   - **Variable**: `SONAR_ORGANIZATION`
   - **Variable**: `SONAR_PROJECT_KEY`
6. Push commit baru, periksa tab **Actions**, dan cek dashboard SonarQube Cloud untuk Quality Gate serta coverage.
7. Buat branch baru di repository yang sama dan ajukan **Pull Request** ke `main` untuk membuktikan trigger PR. Token umumnya tidak tersedia untuk PR dari fork eksternal.

**Catatan:** Workflow memang akan gagal pada tahap validasi konfigurasi SonarQube sebelum secret dan variables dibuat. Ini sengaja agar proses tidak menampilkan status berhasil padahal scanner SonarQube belum berjalan.

## Dokumentasi praktikum

Instruksi screenshot dan tahapan laporan ada pada `PANDUAN_SCREENSHOT_DAN_LAPORAN.md`. Bukti yang wajib berasal dari eksekusi nyata, bukan dibuat berdasarkan perkiraan atau menggunakan screenshot milik orang lain.

## Referensi

- Materi **Integrasi SAST dalam CI/CD Pipeline dengan GitHub Actions**, Pertemuan 5, STT Terpadu Nurul Fikri.
- GitHub Docs: https://docs.github.com/en/actions
- GitHub CodeQL: https://github.com/github/codeql-action
- SonarQube Scan Action: https://github.com/SonarSource/sonarqube-scan-action
