import pytest
from app.validasi import jenis_transaksi, jumlah_rupiah, keterangan_transaksi, tanggal_transaksi

def test_jumlah_rupiah_benar():
    assert jumlah_rupiah("10000") == 10000

@pytest.mark.parametrize("nilai", ["0", "-100", "1.5", "1.000", "satu", True])
def test_jumlah_rupiah_ditolak(nilai):
    with pytest.raises(ValueError):
        jumlah_rupiah(nilai)

def test_jenis_dinormalisasi():
    assert jenis_transaksi(" MASUK ") == "masuk"

def test_jenis_tidak_valid():
    with pytest.raises(ValueError):
        jenis_transaksi("transfer")

def test_keterangan_tidak_boleh_kosong():
    with pytest.raises(ValueError):
        keterangan_transaksi("  ")

def test_tanggal_valid():
    assert tanggal_transaksi("2026-10-20") == "2026-10-20"

def test_tanggal_tidak_valid():
    with pytest.raises(ValueError):
        tanggal_transaksi("20/10/2026")
