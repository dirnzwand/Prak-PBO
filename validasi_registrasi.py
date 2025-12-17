import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# ----------------------------------------------------------------------
# === KONFIGURASI AWAL LOGGING ===
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
# Logger untuk Registrasi
LOGGER = logging.getLogger('registration')

# ----------------------------------------------------------------------
# --- MODEL SEDERHANA ---
# ----------------------------------------------------------------------
@dataclass
class Mahasiswa:
    """Model data sederhana untuk Mahasiswa."""
    nama: str
    total_sks_diambil: int
    lulus_prasyarat: bool
    status_pembayaran: str = "lunas"

# ----------------------------------------------------------------------
# === IMPLEMENTASI SOLID ===
# ----------------------------------------------------------------------

# --- ABSTRAKSI (IValidationRule) ---
class IValidationRule(ABC):
    """
    Kontrak (Interface) yang harus diimplementasikan oleh setiap aturan validasi.
    Memastikan OCP (Open/Closed Principle) terpenuhi.
    """
    @abstractmethod
    def validate(self, mahasiswa: Mahasiswa) -> bool:
        """
        Memvalidasi aturan spesifik pada objek Mahasiswa.
        
        Args:
            mahasiswa (Mahasiswa): Objek mahasiswa yang akan divalidasi.
            
        Returns:
            bool: True jika validasi lolos, False jika gagal.
        """
        pass

# --- IMPLEMENTASI KONKRIT (Mematuhi SRP dan sudah ada Logging) ---
class SKSLimitRule(IValidationRule):
    """Aturan validasi batas maksimum SKS (24 SKS)."""
    def validate(self, mahasiswa: Mahasiswa) -> bool:
        if mahasiswa.total_sks_diambil > 24:
            LOGGER.warning(f"❌ Validasi SKS Gagal untuk {mahasiswa.nama}: Melebihi batas 24 SKS.")
            return False
        LOGGER.info(f"✅ Validasi SKS Lolos untuk {mahasiswa.nama}.")
        return True

class PrasyaratRule(IValidationRule):
    """Aturan validasi kelulusan mata kuliah prasyarat."""
    def validate(self, mahasiswa: Mahasiswa) -> bool:
        if not mahasiswa.lulus_prasyarat:
            LOGGER.warning(f"❌ Validasi Prasyarat Gagal untuk {mahasiswa.nama}.")
            return False
        LOGGER.info(f"✅ Validasi Prasyarat Lolos untuk {mahasiswa.nama}.")
        return True

# --- KELAS KOORDINATOR (RegistrationValidator) ---
class RegistrationValidator:
    """
    Kelas high-level untuk mengkoordinasi eksekusi aturan validasi registrasi.
    Bergantung pada Abstraksi (IValidationRule) melalui Dependency Injection (DIP).
    """
    def __init__(self, rules: list[IValidationRule]):
        """
        Menginisialisasi validator dengan daftar aturan yang di-inject.
        
        Args:
            rules (list[IValidationRule]): List aturan validasi yang akan dijalankan.
        """
        self.rules = rules

    def is_valid(self, mahasiswa: Mahasiswa) -> bool:
        """
        Menjalankan semua aturan validasi yang di-inject secara berurutan.
        
        Args:
            mahasiswa (Mahasiswa): Objek mahasiswa yang akan divalidasi.
            
        Returns:
            bool: True jika semua validasi lolos, False jika ada satu yang gagal.
        """
        LOGGER.info(f"\n--- Memulai Validasi Registrasi untuk {mahasiswa.nama} ---")
        for rule in self.rules:
            if not rule.validate(mahasiswa):
                LOGGER.error(f"Registrasi Gagal Total! Gagal pada aturan: {rule.__class__.__name__}")
                return False
        
        LOGGER.info(f"🎉 Registrasi Sukses! {mahasiswa.nama} disetujui.")
        return True

# ----------------------------------------------------------------------
# === EKSEKUSI DAN PEMBUKTIAN OCP ===
# ----------------------------------------------------------------------
if __name__ == "__main__":
    
    # SETUP AWAL
    rina = Mahasiswa("Rina", 20, True)
    basic_rules = [SKSLimitRule(), PrasyaratRule()]
    validator_basic = RegistrationValidator(basic_rules)
    
    print("--- Skenario 1: Validasi Normal (Rina - Lolos) ---")
    validator_basic.is_valid(rina)
    
    # PEMBUKTIAN OCP: Menambah Aturan Pembayaran Baru
    class PembayaranRule(IValidationRule):
        """Aturan validasi status pembayaran."""
        def validate(self, mahasiswa: Mahasiswa) -> bool:
            if mahasiswa.status_pembayaran != "lunas":
                LOGGER.warning(f"❌ Validasi Pembayaran Gagal untuk {mahasiswa.nama}: Belum lunas.")
                return False
            LOGGER.info(f"✅ Validasi Pembayaran Lolos untuk {mahasiswa.nama}.")
            return True

    budi = Mahasiswa("Budi", 26, True, status_pembayaran="belum_lunas") 
    
    # Menggunakan aturan baru (PembayaranRule) tanpa mengubah RegistrationValidator
    advanced_rules = [SKSLimitRule(), PrasyaratRule(), PembayaranRule()] 
    validator_advanced = RegistrationValidator(advanced_rules)

    print("\n--- Skenario 2: Pembuktian OCP (Budi - Gagal) ---")
    validator_advanced.is_valid(budi)