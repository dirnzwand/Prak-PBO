# main_app.py
import logging
from repositories import ProductRepository
from services import IPaymentProcessor, ShoppingCart, CashPayment, DebitCardPayment
from models import Product # Diperlukan untuk type hint

LOGGER = logging.getLogger('MAIN_APP')

class PosApp:
    """
    Kelas Orchestrator (Aplikasi utama). Hanya mengkoordinasi flow dan menerapkan DI.
    """
    def __init__( 
        self,
        repository: ProductRepository,
        payment_processor: IPaymentProcessor,
    ):
        """
        Menginisialisasi aplikasi dengan dependensi yang di-inject.
        
        Args:
            repository (ProductRepository): Lapisan akses data produk.
            payment_processor (IPaymentProcessor): Lapisan layanan pembayaran (DIP).
        """
        self.repository = repository
        self.payment_processor = payment_processor
        self.cart = ShoppingCart()
        LOGGER.info("POS Application Initialized.")

    def _display_menu(self):
        """Menampilkan daftar produk yang tersedia."""
        LOGGER.info("\n--- DAFTAR PRODUK ---")
        for p in self.repository.get_all():
            LOGGER.info(f"[{p.id}] {p.name} - Rp{p.price:,.0f}")

    def _handle_add_item(self):
        """Memproses input user untuk menambahkan produk ke keranjang."""
        product_id = input("Masukkan ID Produk: ").strip().upper()
        product = self.repository.get_by_id(product_id)

        if not product:
            LOGGER.warning("Produk tidak ditemukan.")
            return
        
        try:
            quantity = int(input("Jumlah (default 1): ") or "1")
            if quantity <= 0:
                raise ValueError
            self.cart.add_item(product, quantity)
        except ValueError:
            LOGGER.error("Jumlah tidak valid.")


    def _handle_checkout(self):
        """Memproses checkout dan pembayaran."""
        total = self.cart.total_price
        
        if total == 0:
            LOGGER.warning("Keranjang kosong.")
            return
        
        LOGGER.info(f"\nTotal Belanja: Rp{total:,.0f}")
        # PENTING: Class PosApp TIDAK DIUBAH, hanya menggunakan payment_processor yang di-inject
        success = self.payment_processor.process(total) 
        
        if success:
            LOGGER.info("TRANSAKSI BERHASIL.")
            self._print_receipt()
            self.cart = ShoppingCart() # Reset cart
        else:
            LOGGER.error("TRANSAKSI GAGAL.")

    def _print_receipt(self):
        """Mencetak struk pembelian."""
        LOGGER.info("\n--- STRUK PEMBELIAN ---")
        for item in self.cart.get_items():
            LOGGER.info(f"{item.product.name} x({item.quantity}) = Rp{item.subtotal:,.0f}")
        LOGGER.info("--------------------------------")
        LOGGER.info(f"TOTAL AKHIR: Rp{self.cart.total_price:,.0f}")
        LOGGER.info("--------------------------------")

# ----------------------------------------------------------------------
# === TITIK MASUK UTAMA (Orchestration & Challenge OCP/DIP) === 
# ----------------------------------------------------------------------
if __name__ == "__main__":
    
    # Setup logging awal
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')

    # 1. Instantiate Lapisan Data
    repo = ProductRepository()

    # 2. Instantiate Service (Menggunakan DebitCardPayment untuk Challenge OCP/DIP)
    payment_method = DebitCardPayment()

    # 3. Inject Dependencies ke Aplikasi Utama
    app = PosApp(repository=repo, payment_processor=payment_method)
    
    # Tambahkan loop CLI sederhana untuk interaksi
    while True:
        print("\nMenu:")
        print("1. Tampilkan Produk")
        print("2. Tambah ke Keranjang")
        print("3. Checkout")
        print("4. Keluar")
        choice = input("Pilih opsi (1-4): ").strip()

        if choice == '1':
            app._display_menu()
        elif choice == '2':
            app._handle_add_item()
        elif choice == '3':
            app._handle_checkout()
        elif choice == '4':
            LOGGER.info("Aplikasi dihentikan.")
            break
        else:
            LOGGER.warning("Pilihan tidak valid.")