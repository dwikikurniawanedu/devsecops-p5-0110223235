"""Baca dan simpan data transaksi dalam format JSON."""
import json
import os
import tempfile
from pathlib import Path

from .models import Transaksi

class PenyimpananJSON:
    def __init__(self, lokasi: str | Path):
        self.lokasi = Path(lokasi)

    def baca(self) -> list[Transaksi]:
        if not self.lokasi.exists():
            return []
        try:
            with self.lokasi.open("r", encoding="utf-8") as berkas:
                data = json.load(berkas)
            if not isinstance(data, list):
                raise ValueError("Isi berkas JSON bukan daftar transaksi.")
            return [Transaksi.dari_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, TypeError) as kesalahan:
            raise ValueError("Berkas transaksi tidak dapat dibaca.") from kesalahan

    def simpan(self, transaksi: list[Transaksi]) -> None:
        self.lokasi.parent.mkdir(parents=True, exist_ok=True)
        nama_sementara = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.lokasi.parent,
                prefix="transaksi-", suffix=".tmp", delete=False,
            ) as berkas:
                nama_sementara = berkas.name
                json.dump([t.menjadi_dict() for t in transaksi], berkas, indent=2, ensure_ascii=False)
            os.replace(nama_sementara, self.lokasi)
        finally:
            if nama_sementara and os.path.exists(nama_sementara):
                os.unlink(nama_sementara)
