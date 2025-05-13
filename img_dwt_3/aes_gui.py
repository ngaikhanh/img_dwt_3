import tkinter as tk
from tkinter import messagebox
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib

def pad(data):
    pad_len = AES.block_size - len(data) % AES.block_size
    return data + bytes([pad_len] * pad_len)

def encrypt_aes(message, key):
    key = hashlib.sha256(key.encode('utf-8')).digest()  # Đảm bảo khóa có độ dài 256 bit
    cipher = AES.new(key, AES.MODE_CBC)  # Sử dụng chế độ CBC
    ct_bytes = cipher.encrypt(pad(message.encode('utf-8')))
    iv = cipher.iv
    return base64.b64encode(iv + ct_bytes).decode('utf-8')

class AESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mã hóa AES")
        self.root.geometry("400x300")

        # Label
        tk.Label(root, text="Khóa bảo mật:", font=("Arial", 12)).pack(pady=5)
        self.key_entry = tk.Entry(root, width=50, show="*")
        self.key_entry.pack()

        tk.Label(root, text="Tin cần mã hóa:", font=("Arial", 12)).pack(pady=5)
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack()

        # Buttons
        tk.Button(root, text="Mã hóa", command=self.encrypt_message).pack(pady=20)

        # Output
        self.output_label = tk.Label(root, text="", font=("Arial", 10), fg="green")
        self.output_label.pack(pady=10)

    def encrypt_message(self):
        key = self.key_entry.get()
        msg = self.message_entry.get()

        if not key or not msg:
            messagebox.showwarning("Thiếu thông tin", "Hãy nhập khóa và tin cần mã hóa.")
            return

        try:
            encrypted_message = encrypt_aes(msg, key)

            # Hiển thị thông điệp mã hóa và khóa bảo mật trên terminal
            print(f"Thông điệp mã hóa (AES): {encrypted_message}")
            # print(f"Khóa bảo mật: {key}")

            # Hiển thị thông điệp mã hóa trên GUI
            self.output_label.config(text=f"Thông điệp mã hóa: {encrypted_message}")
            messagebox.showinfo("Thành công", "Mã hóa AES thành công! Kiểm tra terminal để xem kết quả.")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AESApp(root)
    root.mainloop()
