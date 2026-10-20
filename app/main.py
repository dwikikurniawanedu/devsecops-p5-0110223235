"""Antarmuka perintah terminal untuk pengguna aplikasi."""
import argparse
from pathlib import Path

from .laporan import ekspor_csv, filter_bulan, ringkasan
from .penyimpanan import PenyimpananJSON
from .transaksi import tambah_transaksi, daftar_transaksi, hapus_transaksi

def buat_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Aplikasi pencatatan kas harian")
    parser.add_argument("--file", default="data/transaksi.json", help="Lokasi berkas transaksi JSON")
    perintah = parser.add_subparsers(dest="aksi", required=True)
    tambah = perintah.add_parser("tambah", help="Catat pemasukan atau pengeluaran")
    tambah.add_argument("jenis", choices=["masuk", "keluar"])
    tambah.add_argument("jumlah", help="Nominal dalam rupiah tanpa titik")
    tambah.add_argument("keterangan", help="Keterangan transaksi")
    tambah.add_argument("--tanggal", default=None)
    daftar = perintah.add_parser("daftar", help="Tampilkan seluruh transaksi")
    daftar.add_argument("--jenis", choices=["masuk", "keluar"], default=None)
    laporan = perintah.add_parser("laporan", help="Tampilkan ringkasan saldo")
    laporan.add_argument("--bulan", default=None, help="Filter YYYY-MM")
    hapus = perintah.add_parser("hapus", help="Hapus transaksi berdasarkan ID")
    hapus.add_argument("id", type=int)
    ekspor = perintah.add_parser("ekspor", help="Ekspor transaksi ke berkas CSV")
    ekspor.add_argument("tujuan", help="Lokasi CSV keluaran")
    return parser

def jalankan(argv: list[str] | None = None) -> int:
    argumen = buat_parser().parse_args(argv)
    penyimpanan = PenyimpananJSON(Path(argumen.file))
    try:
        if argumen.aksi == "tambah":
            hasil = tambah_transaksi(penyimpanan, argumen.jenis, argumen.jumlah,
                                   argumen.keterangan, argumen.tanggal)
            print(f"Transaksi #{hasil.id} berhasil ditambahkan.")
        elif argumen.aksi == "daftar":
            data = daftar_transaksi(penyimpanan, argumen.jenis)
            if not data:
                print("Belum ada transaksi.")
            for item in data:
                print(f"#{item.id} | {item.tanggal} | {item.jenis} | Rp{item.jumlah:,} | {item.keterangan}")
        elif argumen.aksi == "laporan":
            data = daftar_transaksi(penyimpanan)
            if argumen.bulan:
                data = filter_bulan(data, argumen.bulan)
            hasil = ringkasan(data)
            print(f"Pemasukan: Rp{hasil['pemasukan']:,}")
            print(f"Pengeluaran: Rp{hasil['pengeluaran']:,}")
            print(f"Saldo: Rp{hasil['saldo']:,}")
        elif argumen.aksi == "hapus":
            berhasil = hapus_transaksi(penyimpanan, argumen.id)
            print("Transaksi berhasil dihapus." if berhasil else "ID transaksi tidak ditemukan.")
        elif argumen.aksi == "ekspor":
            tujuan = ekspor_csv(
                daftar_transaksi(penyimpanan),
                argumen.tujuan,
                Path.cwd() / "exports",
            )
            print(f"Data disimpan ke {tujuan}.")
        return 0
    except ValueError as kesalahan:
        print(f"Kesalahan: {kesalahan}")
        return 1


if __name__ == "__main__":
    raise SystemExit(jalankan())
