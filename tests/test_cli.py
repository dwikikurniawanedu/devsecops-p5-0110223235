from app.main import jalankan

def test_alur_cli(tmp_path, capsys):
    file_data = str(tmp_path / "data.json")
    awal = ["--file", file_data]
    assert jalankan([*awal, "tambah", "masuk", "20000", "Uang saku", "--tanggal", "2026-10-20"]) == 0
    assert jalankan([*awal, "laporan"]) == 0
    assert "Saldo: Rp20,000" in capsys.readouterr().out
    assert jalankan([*awal, "daftar"]) == 0
    assert "Uang saku" in capsys.readouterr().out
    assert jalankan([*awal, "hapus", "1"]) == 0
    assert jalankan([*awal, "daftar"]) == 0
    assert "Belum ada transaksi" in capsys.readouterr().out

def test_cli_angka_invalid(tmp_path, capsys):
    assert jalankan(["--file", str(tmp_path / "data.json"), "tambah", "masuk", "0", "Tidak valid"]) == 1
    assert "Kesalahan" in capsys.readouterr().out

def test_cli_ekspor(tmp_path):
    file_data = str(tmp_path / "data.json")
    file_csv = tmp_path / "ekspor.csv"
    assert jalankan(["--file", file_data, "ekspor", str(file_csv)]) == 0
    assert file_csv.exists()
