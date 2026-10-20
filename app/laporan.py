"""Perhitungan ringkasan kas dan ekspor laporan CSV."""
import csv
from datetime import date
from pathlib import Path

from .models import Transaksi

def ringkasan(transaksi: list[Transaksi]) -> dict[str, int]:
    total_masuk = sum(item.jumlah for item in transaksi if item.jenis == "masuk")
    total_keluar = sum(item.jumlah for item in transaksi if item.jenis == "keluar")
    return {"pemasukan": total_masuk, "pengeluaran": total_keluar,
            "saldo": total_masuk - total_keluar}

def filter_bulan(transaksi: list[Transaksi], bulan: str) -> list[Transaksi]:
    try:
        date.fromisoformat(f"{bulan}-01")
    except ValueError as kesalahan:
        raise ValueError("Bulan harus berformat YYYY-MM.") from kesalahan
    if len(bulan) != 7:
        raise ValueError("Bulan harus berformat YYYY-MM.")
    return [item for item in transaksi if item.tanggal.startswith(bulan + "-")]

def ekspor_csv(transaksi: list[Transaksi], lokasi: str | Path) -> Path:
    tujuan = Path(lokasi)
    tujuan.parent.mkdir(parents=True, exist_ok=True)
    with tujuan.open("w", newline="", encoding="utf-8-sig") as berkas:
        penulis = csv.writer(berkas)
        penulis.writerow(["ID", "Tanggal", "Jenis", "Jumlah (Rp)", "Keterangan"])
        for item in transaksi:
            penulis.writerow([item.id, item.tanggal, item.jenis, item.jumlah, item.keterangan])
    return tujuan
