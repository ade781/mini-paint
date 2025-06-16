# ui/dialogs.py

import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox


class AboutDialog(simpledialog.Dialog):
    """
    Dialog 'Tentang Aplikasi'.
    """

    def body(self, master):
        tk.Label(master, text="Aplikasi Paint Kompleks").pack(pady=5)
        tk.Label(master, text="Versi: 1.0.0").pack(pady=2)
        tk.Label(master, text="Dibuat oleh: Gemini").pack(pady=2)
        tk.Label(master, text="© 2023-2024 Semua Hak Dilindungi.").pack(pady=5)
        return self  # Return widget yang harus memiliki fokus awal

    def buttonbox(self):
        box = tk.Frame(self)
        w = tk.Button(box, text="OK", width=10,
                      command=self.ok, default=tk.ACTIVE)
        w.pack(pady=5)
        self.bind("<Return>", self.ok)
        box.pack()

    def apply(self):
        """Dipanggil saat tombol OK ditekan."""
        pass  # Tidak ada data yang perlu diterapkan dari dialog ini


class ColorPickerDialog(tk.Toplevel):
    """
    Dialog pemilih warna kustom.
    """

    def __init__(self, parent, initial_color: str):
        super().__init__(parent)
        self.transient(parent)  # Membuat dialog muncul di atas jendela induk
        self.grab_set()  # Mengambil semua event input hingga dialog ditutup
        self.parent = parent
        self.result_color = initial_color

        self.title("Pilih Warna")

        self.picker_frame = tk.Frame(self)
        self.picker_frame.pack(padx=10, pady=10)

        # Menggunakan colorchooser bawaan Tkinter
        self.color_box = tk.Label(
            self.picker_frame, text="Warna Saat Ini", bg=self.result_color, width=20, height=5)
        self.color_box.pack(pady=5)

        tk.Button(self.picker_frame, text="Buka Pemilih Warna",
                  command=self._open_tk_color_picker).pack(pady=5)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        tk.Button(self.button_frame, text="OK",
                  command=self._on_ok).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Cancel",
                  command=self._on_cancel).pack(side=tk.RIGHT, padx=5)

        self.wait_window(self)  # Menunggu hingga jendela ini ditutup

    def _open_tk_color_picker(self):
        """Membuka dialog pemilih warna standar Tkinter."""
        color_code = colorchooser.askcolor(self.result_color)
        if color_code[1]:  # color_code[1] adalah nilai heksadesimal
            self.result_color = color_code[1]
            self.color_box.config(bg=self.result_color)

    def _on_ok(self):
        self.parent.focus_set()
        self.destroy()

    def _on_cancel(self):
        self.result_color = None  # Jika dibatalkan, kembalikan None
        self.parent.focus_set()
        self.destroy()

    def get_color(self):
        """Mengembalikan warna yang dipilih."""
        return self.result_color

# Anda bisa menambahkan dialog lain di sini, seperti:
# - SaveConfirmDialog (untuk mengkonfirmasi penyimpanan sebelum keluar)
# - ResizeImageDialog
# - TextPropertiesDialog
