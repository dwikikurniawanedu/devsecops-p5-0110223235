"""Validasi masukan untuk transaksi keuangan sederhana."""
from datetime import date

PILIHAN_JENIS = {"masuk", "keluar"}

def jenis_transaksi(nilai: str) -> str:
    hasil = nilai.strip().lower()
    if hasil not in PILIHAN_JENIS:
        raise ValueError("Jenis transaksi hanya boleh 'masuk' atau 'keluar'.")
    return hasil

def jumlah_rupiah(nilai: str | int) -> int:
    if isinstance(nilai, bool):
        raise ValueError("Jumlah harus bilangan bulat positif.")
    teks = str(nilai).strip()
    if not teks.isascii() or not teks.isdecimal():
        raise ValueError("Jumlah harus bilangan bulat positif.")
    hasil = int(teks)
    if hasil <= 0 or hasil > 1_000_000_000:
        raise ValueError("Jumlah harus antara Rp1 dan Rp1.000.000.000.")
    return hasil

def keterangan_transaksi(nilai: str) -> str:
    hasil = nilai.strip()
    if not hasil or len(hasil) > 120:
        raise ValueError("Keterangan wajib diisi (maksimal 120 karakter).")
    return hasil

def tanggal_transaksi(nilai: str | None = None) -> str:
    if nilai is None:
        return date.today().isoformat()
    try:
        return date.fromisoformat(nilai).isoformat()
    except (TypeError, ValueError) as kesalahan:
        raise ValueError("Tanggal harus menggunakan format YYYY-MM-DD.") from kesalahan
