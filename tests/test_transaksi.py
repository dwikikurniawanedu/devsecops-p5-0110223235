import json
import pytest
from app.penyimpanan import PenyimpananJSON
from app.transaksi import tambah_transaksi, daftar_transaksi, hapus_transaksi

@pytest.fixture
def database(tmp_path):
    return PenyimpananJSON(tmp_path / "transaksi.json")

def test_tambah_transaksi(database):
    item = tambah_transaksi(database, "masuk", "50000", "Uang saku", "2026-10-20")
    assert item.id == 1
    assert database.baca()[0].keterangan == "Uang saku"

def test_id_transaksi_naik(database):
    tambah_transaksi(database, "masuk", 10000, "Tabungan")
    item = tambah_transaksi(database, "keluar", 2500, "Parkir")
    assert item.id == 2

def test_daftar_berdasarkan_jenis(database):
    tambah_transaksi(database, "masuk", 5000, "Kas masuk")
    tambah_transaksi(database, "keluar", 3000, "Makan")
    assert len(daftar_transaksi(database, "keluar")) == 1

def test_hapus_transaksi(database):
    item = tambah_transaksi(database, "keluar", 2000, "Fotokopi")
    assert hapus_transaksi(database, item.id) is True
    assert database.baca() == []

def test_hapus_id_tidak_ada(database):
    assert hapus_transaksi(database, 33) is False

def test_hapus_id_negatif(database):
    with pytest.raises(ValueError):
        hapus_transaksi(database, -1)

def test_data_json_invalid(database):
    database.lokasi.write_text("{rusak", encoding="utf-8")
    with pytest.raises(ValueError):
        database.baca()

def test_data_json_bukan_list(database):
    database.lokasi.write_text(json.dumps({"nilai": 1}), encoding="utf-8")
    with pytest.raises(ValueError):
        database.baca()
