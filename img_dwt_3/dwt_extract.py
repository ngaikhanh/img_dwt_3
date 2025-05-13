import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import pywt
import cv2
import numpy as np
import os
import base64
import hashlib
from Crypto.Cipher import AES

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def decrypt_aes(ciphertext_b64, key_str):
    try:
        raw = base64.b64decode(ciphertext_b64)
        key = hashlib.sha256(key_str.encode('utf-8')).digest()
        iv = raw[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(raw[16:]))
        return pt.decode('utf-8')
    except Exception as e:
        return f"[Lỗi AES] {str(e)}"

def extract_text():
    path = filedialog.askopenfilename(
        title="Chọn ảnh",
        initialdir=os.getcwd(),
        filetypes=[("Ảnh", "*.png;*.jpg;*.jpeg"), ("Tất cả các file", "*.*")]
    )
    if not path:
        return

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        lbl_status.config(text="Không đọc được ảnh!")
        return

    coeffs2 = pywt.dwt2(img, 'haar')
    cA, (cH, cV, cD) = coeffs2

    flat = cH.flatten()
    bits = ''.join([str(int(val) & 1) for val in flat])

    eof_marker = '1111111111111110'
    end_index = bits.find(eof_marker)
    if end_index == -1:
        lbl_status.config(text="Không tìm thấy EOF marker.")
        return
    valid_bits = bits[:end_index]

    byte_array = bytearray(int(valid_bits[i:i+8], 2) for i in range(0, len(valid_bits), 8))
    try:
        extracted_msg = byte_array.decode('utf-8')
    except UnicodeDecodeError:
        lbl_status.config(text="Lỗi giải mã UTF-8.")
        return

    use_aes = messagebox.askyesno("Giải mã AES", "Thông điệp có được mã hóa AES không?")
    if use_aes:
        key = simpledialog.askstring("Nhập khóa", "Nhập khóa AES để giải mã:", show="*")
        if key:
            decrypted_msg = decrypt_aes(extracted_msg, key)
            lbl_status.config(text="Thông điệp đã giải mã:\n" + decrypted_msg)
        else:
            lbl_status.config(text="Bạn đã hủy nhập khóa AES.")
    else:
        lbl_status.config(text="Thông điệp đã trích xuất:\n" + extracted_msg)

root = tk.Tk()
root.title("DWT - Trích xuất tin từ ảnh")
root.geometry("500x300")

btn = tk.Button(root, text="Chọn ảnh và trích xuất", command=extract_text)
btn.pack(pady=10)

lbl_status = tk.Label(root, text="", wraplength=400, justify="left")
lbl_status.pack(pady=10)

root.mainloop()

