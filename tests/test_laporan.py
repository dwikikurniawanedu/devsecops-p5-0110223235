import csv
import pytest
from app.models import Transaksi
from app.laporan import ringkasan, filter_bulan, ekspor_csv

@pytest.fixture
def sampel():
    return [
        Transaksi(1, "2026-10-01", "masuk", 100000, "Gaji"),
        Transaksi(2, "2026-10-03", "keluar", 25000, "Makan"),
        Transaksi(3, "2026-09-27", "keluar", 5000, "Parkir"),
    ]

def test_ringkasan(sampel):
    assert ringkasan(sampel) == {"pemasukan": 100000, "pengeluaran": 30000, "saldo": 70000}

def test_filter_bulan(sampel):
    assert len(filter_bulan(sampel, "2026-10")) == 2

def test_filter_bulan_tidak_valid(sampel):
    with pytest.raises(ValueError):
        filter_bulan(sampel, "Oktober 2026")

def test_ekspor_csv(sampel, tmp_path):
    tujuan = ekspor_csv(sampel, tmp_path / "hasil.csv")
    with tujuan.open(encoding="utf-8-sig", newline="") as berkas:
        hasil = list(csv.reader(berkas))
    assert hasil[0][0] == "ID"
    assert len(hasil) == 4
