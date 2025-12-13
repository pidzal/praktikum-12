import logging
# [pastikan import looging ada diawal file]

# konfigurasi dasar: semua log level INFO keatas akan ditampilkan
# format: waktu - level - Nama/Fungsi - pesan
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(massage)s'
)
# tambahkan logger untuk kelas yang akan kita gunakan
LOGGER = logging.getLogger('Checkout')

from abc import ABC, abstractmethod 
from dataclasses import dataclass

# Model Sederhana
@dataclass
class Order:
    customer_name: str
    total_price: float
    status: str = "open"

# === KODE BURUK (SEBELUM REFACTOR) ===
class OrderManager:  # Melanggar SRP, OCP, DIP
    def process_checkout(self, order: Order, payment_method: str):
        print(f"Memulai checkout untuk {order.customer_name}...")

        # LOGIKA PEMBAYARAN (Pelanggaran OCP/DIP)
        if payment_method == "credit_card":
            # Logika detail implementasi hardcoded di sini
            print("Processing Credit Card...")
        elif payment_method == "bank_transfer":
            # Logika detail implementasi hardcoded di sini
            print("Processing Bank Transfer...")
        else:
            print("Metode tidak valid.")
            return False

        # LOGIKA NOTIFIKASI (Pelanggaran SRP)
        print(f"Mengirim notifikasi ke {order.customer_name}...")
        order.status = "paid"
        return True
    
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
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses Kartu Kredit.")
        return True


class EmailNotifier(INotificationService):
    def send(self, order: Order):
        print(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")


# --- KELAS KOORDINATOR (SRP & DIP) ---
class CheckoutService:  # Tanggung jawab tunggal: Mengkoordinasi Checkout
    """
    kelas high-level untuk mengkoordinasi proses transaksi pembayaran
    kelas ini memisahkan logika pembayaran dan notifikasi (memenuhi SRP)
    """
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        """
        meninisiasikan CheckoutService dengan dependensi yang di perlukan
        
        Args:
            payment_processor (IPaymentProcessor): implementasi interface pembayaran.
            notifier (INotificationService): implementasi interface notifikasi
        """
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order) -> bool:
        # looging alih-alih print()
        LOGGER.info(f"Memulai checkout untuk {order.customer_name}. total: {order.total_price}")
        
        payment_success = self.payment_processor.process(order)  # Delegasi 1

        if payment_success:
            order.status = "paid"
            self.notifier.send(order)  # Delegasi 2
            print("Checkout Sukses.")
            return True
        else:
            # gunakan level ERROR/WARNING untuk masalah
            LOGGER.error("pembayaran gagal. transaksi dibatalkan")
            return False

# --- PROGRAM UTAMA ---
# Setup Dependencies
andi_order = Order("Andi", 500000)
email_service = EmailNotifier()

# 1. Inject implementasi Credit Card
cc_processor = CreditCardProcessor()
checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)
print("\n--- Skenario 1: Credit Card ---")
checkout_cc.run_checkout(andi_order)

# 2. Pembuktian OCP: Menambah Metode Pembayaran QRIS (Tanpa Mengubah CheckoutService)
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
