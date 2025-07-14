import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.title("CyberAlbertou Siber Güvenlik Aracı")

output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(pady=10)

output_text.insert(tk.END, "[✓] CyberAlbertou GUI başlatıldı.\n")

root.mainloop()
