import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# ----------------------------------------------------------------------
# === KONFIGURASI AWAL (Langkah 2 Logging) ===
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
LOGGER = logging.getLogger('checkout')

# ----------------------------------------------------------------------
# --- MODEL SEDERHANA ---
# ----------------------------------------------------------------------
@dataclass
class Order:
    """Model data sederhana untuk Order."""
    customer_name: str
    total_price: float
    status: str = "open"

# ----------------------------------------------------------------------
# === IMPLEMENTASI SOLID ===
# ----------------------------------------------------------------------

# --- ABSTRAKSI (Kontrak untuk OCP/DIP) ---
class IPaymentProcessor(ABC):
    """Kontrak: Semua prosesor pembayaran harus punya method 'process'."""
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

class INotificationService(ABC):
    """Kontrak: Semua layanan notifikasi harus punya method 'send'."""
    @abstractmethod
    def send(self, order: Order):
        pass

# --- IMPLEMENTASI KONKRIT (Mematuhi SRP) ---
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        LOGGER.info("Payment: Memproses Kartu Kredit.")
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        LOGGER.info(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")

# --- KELAS KOORDINATOR (Mematuhi SRP & DIP) ---
class CheckoutService:
    """
    Kelas high-level untuk mengkoordinasi proses transaksi pembayaran.
    Memisahkan logika pembayaran dan notifikasi (memenuhi SRP).
    """
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        """
        Args:
            payment_processor (IPaymentProcessor): Implementasi Interface pembayaran.
            notifier (INotificationService): Implementasi Interface notifikasi.
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order) -> bool:
        """
        Menjalankan proses checkout dan memvalidasi pembayaran.
        
        Args:
            order (Order): Objek pesanan yang akan diproses.
            
        Returns:
            bool: True jika checkout sukses, False jika gagal.
        """
        LOGGER.info(f"Memulai checkout untuk {order.customer_name}. Total: {order.total_price}")
        payment_success = self.payment_processor.process(order)

        if payment_success:
            order.status = "paid"
            self.notifier.send(order)
            LOGGER.info("Checkout Sukses. Status pesanan: PAID.")
            return True
        else:
            LOGGER.error("Pembayaran gagal. Transaksi dibatalkan.")
            return False

# ----------------------------------------------------------------------
# === EKSEKUSI DAN PEMBUKTIAN OCP (Langkah 3) ===
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Skenario 1: Credit Card
    andi_order = Order("Andi", 500000)
    email_service = EmailNotifier()
    cc_processor = CreditCardProcessor()
    
    checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)
    print("\n--- Skenario 1: Credit Card (Log akan muncul di atas) ---")
    checkout_cc.run_checkout(andi_order)

    # PEMBUKTIAN OCP: Menambah Metode Pembayaran QRIS (Tanpa Mengubah CheckoutService)
    class QrisProcessor(IPaymentProcessor):
        def process(self, order: Order) -> bool:
            LOGGER.info("Payment: Memproses QRIS.")
            return True

    # Skenario 2: QRIS
    budi_order = Order("Budi", 100000)
    qris_processor = QrisProcessor()
    
    checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service)
    print("\n--- Skenario 2: Pembuktian OCP (QRIS) ---")
    checkout_qris.run_checkout(budi_order)