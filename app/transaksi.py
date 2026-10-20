"""Aturan tambah, lihat, dan hapus transaksi kas."""
from .models import Transaksi
from .penyimpanan import PenyimpananJSON
from .validasi import jumlah_rupiah, jenis_transaksi, keterangan_transaksi, tanggal_transaksi

def tambah_transaksi(
    penyimpanan: PenyimpananJSON, jenis: str, jumlah: str | int,
    keterangan: str, tanggal: str | None = None,
) -> Transaksi:
    daftar = penyimpanan.baca()
    id_baru = max((item.id for item in daftar), default=0) + 1
    baru = Transaksi(
        id=id_baru,
        tanggal=tanggal_transaksi(tanggal),
        jenis=jenis_transaksi(jenis),
        jumlah=jumlah_rupiah(jumlah),
        keterangan=keterangan_transaksi(keterangan),
    )
    penyimpanan.simpan([*daftar, baru])
    return baru

def daftar_transaksi(penyimpanan: PenyimpananJSON, jenis: str | None = None) -> list[Transaksi]:
    data = penyimpanan.baca()
    if jenis is not None:
        kategori = jenis_transaksi(jenis)
        data = [item for item in data if item.jenis == kategori]
    return sorted(data, key=lambda item: (item.tanggal, item.id))

def hapus_transaksi(penyimpanan: PenyimpananJSON, identitas: int) -> bool:
    if identitas <= 0:
        raise ValueError("ID harus bilangan positif.")
    daftar = penyimpanan.baca()
    hasil = [item for item in daftar if item.id != identitas]
    if len(daftar) == len(hasil):
        return False
    penyimpanan.simpan(hasil)
    return True
