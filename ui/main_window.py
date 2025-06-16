# ui/main_window.py

import tkinter as tk
from tkinter import filedialog
from tkinter import colorchooser
import os
import time  # Import time untuk mensimulasikan jeda atau debugging waktu

# Import dari config
from config import AppConfig

# Import dari core
from core.canvas_manager import CanvasManager
# from core.application import Application # Tidak perlu import melingkar, Application akan meneruskan dirinya sendiri

# Import dari ui lainnya
from ui.menus import MainMenu
from ui.toolbars import ToolbarPanel
from ui.dialogs import AboutDialog, ColorPickerDialog


class MainWindow:
    """
    Mengelola jendela utama aplikasi dan tata letak UI keseluruhan.
    """

    def __init__(self, root: tk.Tk, app_instance):
        """
        Inisialisasi jendela utama.

        Args:
            root (tk.Tk): Objek Tkinter root window.
            app_instance: Instance dari kelas Application.
        """
        self.root = root
        self.app = app_instance

        # --- Tampilan Loading Awal ---
        self.loading_frame = tk.Frame(self.root, bg="#333333")
        self.loading_frame.pack(fill="both", expand=True)

        tk.Label(self.loading_frame, text="Aplikasi Paint Kompleks - Membangun...",
                 fg="white", bg="#333333", font=("Arial", 16)).pack(pady=50)
        tk.Label(self.loading_frame, text="Mohon tunggu sebentar...",
                 fg="white", bg="#333333", font=("Arial", 12)).pack(pady=10)

        # Paksa Tkinter untuk memperbarui jendela agar frame loading terlihat segera
        self.root.update_idletasks()
        # Untuk tujuan demonstrasi, tambahkan jeda singkat
        # time.sleep(1) # Hapus atau komen ini untuk penggunaan produksi

        print("MainWindow: Loading frame ditampilkan.")

        # --- Lanjutkan Inisialisasi UI Utama ---
        # Ini akan dilakukan setelah jeda/pemrosesan simulasi selesai
        self._create_main_frames()

        # Set teks awal di status bar
        self.update_status("Siap.")  # Status bar kembali ke "Siap."

        # Set title bar dengan tambahan "Made by ade7"
        # Menampilkan di title bar
        self.root.title(f"{AppConfig.WINDOW_TITLE} - Made by ade7")

        # Setelah semua frame utama dibuat, sembunyikan/hapus loading frame
        self.loading_frame.destroy()
        print("MainWindow: Loading frame disembunyikan. UI utama ditampilkan.")

        # Catatan: canvas_manager, main_menu, dan toolbar_panel diinisialisasi oleh Application
        # dan referensinya akan tersedia melalui self.app.canvas_manager, dll.

        print("MainWindow diinisialisasi. Frames UI utama dibuat.")

    def _create_main_frames(self):
        """
        Membuat frame utama untuk tata letak UI.
        """
        # Frame atas untuk toolbar
        self.top_frame = tk.Frame(self.root, bd=2, relief=tk.RAISED)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        print("MainWindow: Top frame untuk toolbar dibuat.")

        # Frame untuk kanvas gambar
        self.canvas_frame = tk.Frame(
            self.root, bd=2, relief=tk.SUNKEN, bg="gray")
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH,
                               expand=True, padx=5, pady=5)
        print("MainWindow: Canvas frame dibuat.")

        # Frame bawah untuk status bar atau kontrol tambahan
        self.bottom_frame = tk.Frame(self.root, bd=2, relief=tk.SUNKEN)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        # Label status bar, akan diinisialisasi dengan pesan default
        # Diubah agar teks awal diatur setelahnya
        self.status_label = tk.Label(self.bottom_frame, text="", anchor="w")
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        print("MainWindow: Bottom frame dan status bar dibuat.")

    def update_status(self, message: str):
        """
        Memperbarui teks di status bar.
        """
        self.status_label.config(text=message)
        # print(f"Status diperbarui: {message}") # Jangan terlalu banyak print di status update

    # Metode untuk menangani aksi menu dan toolbar
    def open_file(self):
        """
        Membuka dialog untuk memilih dan membuka file gambar.
        """
        file_path = filedialog.askopenfilename(
            initialdir=".",
            title="Pilih Gambar",
            filetypes=(
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*"))
        )
        if file_path:
            self.app.open_image(file_path)
            # self.update_status(f"Membuka: {os.path.basename(file_path)}") # Sudah dihandle di app.open_image

    def save_file(self):
        """
        Membuka dialog untuk menyimpan gambar ke file.
        """
        file_path = filedialog.asksaveasfilename(
            initialdir=".",
            title="Simpan Gambar Sebagai",
            defaultextension=".png",
            filetypes=(("PNG files", "*.png"),
                       ("JPEG files", "*.jpg"), ("All files", "*.*"))
        )
        if file_path:
            self.app.save_image(file_path)
            # self.update_status(f"Menyimpan: {os.path.basename(file_path)}") # Sudah dihandle di app.save_image

    def show_about_dialog(self):
        """
        Menampilkan dialog 'Tentang Aplikasi'.
        """
        AboutDialog(self.root)

    def show_color_picker(self):
        """
        Menampilkan dialog pemilih warna.
        """
        selected_color_tuple, selected_color_hex = colorchooser.askcolor(
            parent=self.root, initialcolor=self.app.current_color)
        # Pastikan pengguna memilih warna (bukan membatalkan)
        if selected_color_hex:
            self.app.set_color(selected_color_hex)
