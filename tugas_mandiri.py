import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


# ================= MODEL =================
@dataclass
class User:
    name: str
    phone: str
    email: str


# ================= KODE BURUK (SEBELUM REFACTOR) =================
class NotificationManager:  # Melanggar SRP, OCP, DIP
    def send_notification(self, user: User, notif_type: str, message: str):
        logging.INFO(f"Menyiapkan notifikasi untuk {user.name}...")

        if notif_type == "email":
            logging.INFO(f"[EMAIL] Mengirim email ke {user.email} dengan pesan: {message}")

        elif notif_type == "sms":
            logging.INFO(f"[SMS] Mengirim SMS ke {user.phone} dengan pesan: {message}")

        elif notif_type == "whatsapp":
            logging.INFO(f"[WA] Mengirim WhatsApp ke {user.phone} dengan pesan: {message}")

        else:
            logging.WARNING("Tipe notifikasi tidak valid.")
            return False

        logging.INFO("Notifikasi terkirim.")
        return True


# ================= ABSTRAKSI =================
class INotificationSender(ABC):
    """
    Interface untuk seluruh layanan pengiriman notifikasi.

    Setiap class yang mengimplementasikan interface ini
    wajib menyediakan method send().
    """

    @abstractmethod
    def send(self, user: User, message: str):
        """
        Mengirim notifikasi ke pengguna.

        Args:
            user (User): Data pengguna penerima notifikasi.
            message (str): Pesan yang akan dikirim.

        Returns:
            None
        """
        pass


# ================= IMPLEMENTASI KONKRIT =================
class EmailNotification(INotificationSender):
    def send(self, user: User, message: str):
        logging.INFO(f"[EMAIL] Mengirim email ke {user.email}: {message}")


class SMSNotification(INotificationSender):
    def send(self, user: User, message: str):
        logging.INFO(f"[SMS] Mengirim SMS ke {user.phone}: {message}")


class WhatsAppNotification(INotificationSender):
    def send(self, user: User, message: str):
        logging.INFO(f"[WHATSAPP] Mengirim WhatsApp ke {user.phone}: {message}")


# ================= SERVICE =================
class NotificationService:
    """
    Service untuk mengoordinasikan proses pengiriman notifikasi.

    Class ini hanya bertanggung jawab mengatur alur pengiriman
    dan tidak bergantung pada implementasi konkret notifikasi.
    """

    def __init__(self, sender: INotificationSender):
        """
        Konstruktor NotificationService.

        Args:
            sender (INotificationSender): Implementasi layanan
            notifikasi yang akan digunakan.
        """
        self.sender = sender

    def notify(self, user: User, message: str):
        """
        Menjalankan proses pengiriman notifikasi.

        Args:
            user (User): Pengguna penerima notifikasi.
            message (str): Pesan notifikasi.

        Returns:
            None
        """
        self.sender.send(user, message)
        logging.INFO("Notifikasi berhasil dikirim.\n")


# ================= PROGRAM UTAMA =================
andi = User(name="Andi", phone="08123456789", email="andi@mail.com")

# Email
email_service = NotificationService(EmailNotification())
logging.INFO("--- Skenario 1: Notifikasi via Email ---")
email_service.notify(andi, "Pesanan Anda telah diproses.")

# WhatsApp
wa_service = NotificationService(WhatsAppNotification())
logging.INFO("--- Skenario 2: Notifikasi via WhatsApp ---")
wa_service.notify(andi, "Barang sudah dikirim.")


# ================= PEMBUKTIAN OCP =================
class TelegramNotification(INotificationSender):
    def send(self, user: User, message: str):
        logging.INFO(f"[TELEGRAM] Mengirim Telegram ke {user.phone}: {message}")

budi = User(name="Budi", phone="0899991111", email="budi@mail.com")
telegram_service = NotificationService(TelegramNotification())

logging.INFO("--- Skenario 3: Pembuktian OCP (Telegram) ---")
telegram_service.notify(budi, "Saldo Anda telah bertambah.")
