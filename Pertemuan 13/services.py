# services.py
from abc import ABC, abstractmethod
import logging
from typing import List, Dict
from models import Product, CartItem # Wajib diimpor dari models.py

# Konfigurasi Logger (Pastikan sudah diinisialisasi di main_app.py)
LOGGER = logging.getLogger('SERVICES') # Logger untuk layanan

# ----------------------------------------------------------------------
# --- INTERFACE PEMBAYARAN (DIP/OCP) ---
# ----------------------------------------------------------------------
class IPaymentProcessor(ABC):
    """Kontrak untuk proses pembayaran apa pun."""
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

# --- IMPLEMENTASI KONKRIT (SRP) ---
class CashPayment(IPaymentProcessor):
    """Implementasi konkrit untuk pembayaran tunai."""
    def process(self, amount: float) -> bool:
        LOGGER.info(f"Menerima Tunai sejumlah: Rp{amount:,.0f}")
        return True

# --- IMPLEMENTASI BARU (Challenge OCP/DIP) ---
class DebitCardPayment(IPaymentProcessor):
    """Implementasi konkrit untuk pembayaran Kartu Debit."""
    def process(self, amount: float) -> bool:
        LOGGER.info(f"Mencoba Debit Card Payment sejumlah: Rp{amount:,.0f}")
        # Logika pembayaran debit
        LOGGER.info("Debit Card payment processed successfully.")
        return True

# ----------------------------------------------------------------------
# --- SERVICE KERANJANG BELANJA (Logika Inti Bisnis - SRP) ---
# ----------------------------------------------------------------------
class ShoppingCart:
    """
    Mengelola item, kuantitas, dan total harga pesanan (SRP).
    """
    def __init__(self):
        self._items: Dict[str, CartItem] = {} # Menggunakan Product ID sebagai key

    def add_item(self, product: Product, quantity: int = 1):
        """Menambah item ke keranjang. Jika produk sudah ada, kuantitas diperbarui."""
        if product.id in self._items:
            self._items[product.id].quantity += quantity
        else:
            self._items[product.id] = CartItem(product=product, quantity=quantity)
        
        LOGGER.info(f"Added {quantity}x {product.name} to cart.")

    def get_items(self) -> List[CartItem]:
        """Mengambil daftar semua item di keranjang."""
        return list(self._items.values())

    @property
    def total_price(self) -> float:
        """Menghitung total harga semua item di keranjang."""
        return sum(item.subtotal for item in self._items.values())