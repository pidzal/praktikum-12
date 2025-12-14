from abc import ABC, abstractmethod
from dataclasses import dataclass

# Model Sederhana
@dataclass
class User:
    name: str
    phone: str
    email: str


# === KODE BURUK (SEBELUM REFACTOR) ===
class NotificationManager:  # Melanggar SRP, OCP, DIP
    def send_notification(self, user: User, notif_type: str, message: str):
        print(f"Menyiapkan notifikasi untuk {user.name}...")

        # LOGIKA NOTIFIKASI (Pelanggaran OCP + DIP)
        if notif_type == "email":
            print(f"[EMAIL] Mengirim email ke {user.email} dengan pesan: {message}")

        elif notif_type == "sms":
            print(f"[SMS] Mengirim SMS ke {user.phone} dengan pesan: {message}")

        elif notif_type == "whatsapp":
            print(f"[WA] Mengirim WhatsApp ke {user.phone} dengan pesan: {message}")

        else:
            print("Tipe notifikasi tidak valid.")
            return False

        print("Notifikasi terkirim.")
        return True



# === ABSTRAKSI (Kontrak untuk OCP/DIP) ===

class INotificationSender(ABC):
    """Kontrak: setiap jenis layanan notifikasi wajib punya method send()."""
    @abstractmethod
    def send(self, user: User, message: str):
        pass



# === IMPLEMENTASI KONKRIT (Plug-in) ===

class EmailNotification(INotificationSender):
    def send(self, user: User, message: str):
        print(f"[EMAIL] Mengirim email ke {user.email}: {message}")


class SMSNotification(INotificationSender):
    def send(self, user: User, message: str):
        print(f"[SMS] Mengirim SMS ke {user.phone}: {message}")


class WhatsAppNotification(INotificationSender):
    def send(self, user: User, message: str):
        print(f"[WHATSAPP] Mengirim WhatsApp ke {user.phone}: {message}")



# === KELAS KOORDINATOR (SRP + DIP) ===

class NotificationService:
    """Tanggung jawab tunggal: Mengatur proses pengiriman notifikasi."""
    def __init__(self, sender: INotificationSender):
        # DIP: bergantung pada abstraksi, bukan implementasi konkret
        self.sender = sender

    def notify(self, user: User, message: str):
        self.sender.send(user, message)
        print("Notifikasi berhasil dikirim.\n")



# --- PROGRAM UTAMA ---

andi = User(name="Andi", phone="08123456789", email="andi@mail.com")

# 1. Gunakan Email
email_sender = EmailNotification()
email_service = NotificationService(sender=email_sender)

print("\n--- Skenario 1: Notifikasi via Email ---")
email_service.notify(andi, "Pesanan Anda telah diproses.")


# 2. Gunakan WhatsApp
wa_sender = WhatsAppNotification()
wa_service = NotificationService(sender=wa_sender)

print("\n--- Skenario 2: Notifikasi via WhatsApp ---")
wa_service.notify(andi, "Barang sudah dikirim.")


# === PEMBUKTIAN OCP ===
# Tambah metode baru (Telegram) tanpa mengubah NotificationService

class TelegramNotification(INotificationSender):
    def send(self, user: User, message: str):
        print(f"[TELEGRAM] Mengirim Telegram ke {user.phone}: {message}")

budi = User(name="Budi", phone="0899991111", email="budi@mail.com")

telegram_sender = TelegramNotification()
telegram_service = NotificationService(sender=telegram_sender)

print("\n--- Skenario 3: Pembuktian OCP (Telegram) ---")
telegram_service.notify(budi, "Saldo Anda telah bertambah.")