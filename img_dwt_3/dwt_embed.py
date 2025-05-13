import tkinter as tk
from tkinter import filedialog
import pywt
import cv2
import numpy as np
import os

def embed_text():
    path = filedialog.askopenfilename(
    title="Chọn ảnh",
    initialdir=os.getcwd(),
    filetypes=[("Tất cả các file", "*.*"), ("Ảnh PNG", "*.png"), ("Ảnh JPG", "*.jpg;*.jpeg")]
)
    if not path:
        return

    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        lbl_status.config(text="Không đọc được ảnh!")
        return

    message = entry.get()
    if not message:
        lbl_status.config(text="Vui lòng nhập nội dung cần giấu.")
        return

    bin_msg = ''.join(format(byte, '08b') for byte in message.encode('utf-8')) + '1111111111111110'
    coeffs2 = pywt.dwt2(img, 'haar')
    cA, (cH, cV, cD) = coeffs2

    flat = cH.flatten()
    if len(bin_msg) > len(flat):
        lbl_status.config(text="Tin quá dài để giấu trong ảnh này.")
        return

    for i in range(len(bin_msg)):
        flat[i] = int(flat[i]) & ~1 | int(bin_msg[i])
    cH_mod = flat.reshape(cH.shape)

    coeffs2_mod = (cA, (cH_mod, cV, cD))
    img_stego = pywt.idwt2(coeffs2_mod, 'haar')
    img_stego = np.uint8(np.clip(img_stego, 0, 255))

    out_path = os.path.join(os.getcwd(), "stego.png")
    cv2.imwrite(out_path, img_stego)
    lbl_status.config(text=f"Đã giấu tin vào ảnh: {out_path}")

root = tk.Tk()
root.title("DWT - Giấu tin vào ảnh")
root.geometry("500x300")

entry = tk.Entry(root, width=50)
entry.pack(pady=10)
btn = tk.Button(root, text="Chọn ảnh và giấu tin", command=embed_text)
btn.pack(pady=5)
lbl_status = tk.Label(root, text="")
lbl_status.pack(pady=5)

root.mainloop()
