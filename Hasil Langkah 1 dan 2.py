from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- MODEL SEDERHANA ---
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

# ----------------------------------------------------------------------
# === KODE AWAL BERMASALAH (Langkah 1: The God Class) ===
# ----------------------------------------------------------------------
# Kode ini melanggar SRP (karena menangani pembayaran, notifikasi, dan checkout)
# dan OCP/DIP (karena menggunakan if/else untuk logika pembayaran).
# 
# class OrderManager: 
#     def process_checkout(self, order: Order, payment_method: str):
#         print(f"Memulai checkout untuk {order.customer_name}...")
# 
#         if payment_method == "credit_card":
#             print("Processing Credit Card...")
#         elif payment_method == "bank_transfer":
#             print("Processing Bank Transfer...")
#         else:
#             print("Metode tidak valid.")
#             return False
# 
#         print(f"Mengirim notifikasi ke {order.customer_name}...")
#         order.status = "paid"
#         return True

# ----------------------------------------------------------------------
# === SOLUSI REFACTORING (Langkah 2: Abstraksi, SRP, DIP) ===
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

# --- IMPLEMENTASI KONKRIT (Plug-in) ---
class CreditCardProcessor(IPaymentProcessor): # Mematuhi SRP
    def process(self, order: Order) -> bool:
        print("Payment: Memproses Kartu Kredit.")
        return True

class EmailNotifier(INotificationService): # Mematuhi SRP
    def send(self, order: Order):
        print(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")

# --- KELAS KOORDINATOR (SRP & DIP) ---
class CheckoutService:
    """
    Kelas high-level untuk mengkoordinasi proses transaksi pembayaran.
    Kelas ini memisahkan logika pembayaran dan notifikasi (memenuhi SRP).
    """
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        """
        Args:
            payment_processor (IPaymentProcessor): Implementasi Interface pembayaran.
            notifier (INotificationService): Implementasi Interface notifikasi.
        """
        # Dependency Injection (DIP): Bergantung pada Abstraksi
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
        payment_success = self.payment_processor.process(order) # Delegasi 1

        if payment_success:
            order.status = "paid"
            self.notifier.send(order) # Delegasi 2
            print("Checkout Sukses.")
            return True
        return False

# ----------------------------------------------------------------------
# === EKSEKUSI DAN PEMBUKTIAN OCP (Langkah 3) ===
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Setup Dependencies
    andi_order = Order("Andi", 500000)
    email_service = EmailNotifier()

    # 1. Inject implementasi Credit Card
    cc_processor = CreditCardProcessor()
    checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)
    print("--- Skenario 1: Credit Card ---")
    checkout_cc.run_checkout(andi_order)

    # 2. Pembuktian OCP: Menambah Metode Pembayaran QRIS (Tanpa Mengubah CheckoutService)
    # Ini membuktikan Open/Closed Principle: Buka untuk ekstensi, Tutup untuk modifikasi.
    class QrisProcessor(IPaymentProcessor):
        def process(self, order: Order) -> bool:
            print("Payment: Memproses QRIS.")
            return True

    budi_order = Order("Budi", 100000)
    qris_processor = QrisProcessor()

    # Inject implementasi QRIS yang baru dibuat
    checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service)
    print("\n--- Skenario 2: Pembuktian OCP (QRIS) ---")
    checkout_qris.run_checkout(budi_order)