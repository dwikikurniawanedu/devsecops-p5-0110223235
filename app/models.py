"""Representasi satu transaksi dalam aplikasi."""
from dataclasses import asdict, dataclass

@dataclass(frozen=True)
class Transaksi:
    id: int
    tanggal: str
    jenis: str
    jumlah: int
    keterangan: str

    def menjadi_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def dari_dict(cls, data: dict) -> "Transaksi":
        return cls(
            id=int(data["id"]),
            tanggal=str(data["tanggal"]),
            jenis=str(data["jenis"]),
            jumlah=int(data["jumlah"]),
            keterangan=str(data["keterangan"]),
        )
