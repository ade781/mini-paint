# src/app.py

import tkinter as tk
from tkinter import colorchooser, ttk  # Menggunakan ttk untuk widget modern
import os  # Untuk operasi file seperti menyimpan gambar
from src.drawing_canvas import DrawingCanvas
from src.ui_components import UIComponents


class PaintApp:
    """
    Kelas utama untuk aplikasi Paint.
    Mengatur jendela utama, kanvas gambar, dan interaksi UI.
    """

    def __init__(self, master):
        """
        Inisialisasi aplikasi Paint.

        Args:
            master (tk.Tk): Objek jendela utama Tkinter.
        """
        self.master = master
        self.master.title("Mini Paint App")
        # Mengatur ukuran jendela awal
        self.master.geometry("800x600")

        # Variabel untuk status drawing
        self.current_color = "black"
        self.brush_size = 5
        self.is_eraser_mode = False

        self._create_widgets()

    def _create_widgets(self):
        """
        Membuat dan menempatkan semua widget di jendela aplikasi.
        """
        # Frame untuk toolbar
        self.toolbar_frame = ttk.Frame(
            self.master, relief=tk.RAISED, borderwidth=2)
        self.toolbar_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Inisialisasi UIComponents (Toolbar)
        self.ui_components = UIComponents(
            self.toolbar_frame,
            on_color_pick=self._choose_color,
            on_brush_size_change=self._set_brush_size,
            on_toggle_eraser=self._toggle_eraser_mode,
            on_clear_canvas=self._clear_canvas,
            on_save_image=self._save_image
        )

        # Kanvas gambar
        self.drawing_canvas = DrawingCanvas(
            self.master,
            bg="white",
            height=500,  # Ukuran kanvas awal
            width=780,
            current_color=self.current_color,
            brush_size=self.brush_size
        )
        self.drawing_canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _choose_color(self):
        """
        Membuka dialog pemilihan warna dan mengatur warna kuas.
        """
        color_code = colorchooser.askcolor(title="Pilih Warna")
        if color_code[1]:  # Jika pengguna memilih warna (bukan membatalkan)
            self.current_color = color_code[1]
            self.drawing_canvas.set_color(self.current_color)
            print(f"Warna diubah menjadi: {self.current_color}")

    def _set_brush_size(self, size):
        """
        Mengatur ukuran kuas berdasarkan input slider.

        Args:
            size (str): Ukuran kuas dari slider (string, perlu diubah ke int).
        """
        self.brush_size = int(
            float(size))  # Konversi dari string ke float lalu int
        self.drawing_canvas.set_brush_size(self.brush_size)
        print(f"Ukuran kuas diubah menjadi: {self.brush_size}")

    def _toggle_eraser_mode(self):
        """
        Mengaktifkan atau menonaktifkan mode penghapus.
        """
        self.is_eraser_mode = not self.is_eraser_mode
        self.drawing_canvas.toggle_eraser(self.is_eraser_mode)
        print(
            f"Mode penghapus: {'Aktif' if self.is_eraser_mode else 'Nonaktif'}")
        # Perbarui tampilan tombol atau indikator mode penghapus jika ada

    def _clear_canvas(self):
        """
        Membersihkan seluruh isi kanvas.
        """
        self.drawing_canvas.clear_canvas()
        print("Kanvas dibersihkan.")

    def _save_image(self):
        """
        Menyimpan gambar dari kanvas.
        Untuk fitur ini, kita perlu Pillow (PIL).
        """
        print("Fungsi simpan gambar akan diimplementasikan di sini.")
        # Catatan: Menyimpan kanvas di Tkinter membutuhkan library eksternal seperti Pillow (PIL).
        # Kamu perlu menginstal 'Pillow' dengan: pip install Pillow
        # Implementasi detail akan memerlukan konversi dari postscript ke format gambar.
        # Untuk kesederhanaan awal, kita akan menandainya sebagai TODO.

        # Contoh dasar (membutuhkan Pillow dan Ghostscript untuk format non-EPS/PS)
        # try:
        #     from PIL import Image, ImageDraw
        #     # Mendapatkan bounding box dari semua item di kanvas
        #     x1, y1, x2, y2 = self.drawing_canvas.canvas.bbox("all")
        #     if x1 is None: # Kanvas kosong
        #         print("Kanvas kosong, tidak ada yang bisa disimpan.")
        #         return

        #     # Membuat gambar Pillow baru dengan ukuran yang sesuai
        #     # Perlu logika yang lebih canggih untuk mendapatkan konten pixel dari Canvas Tkinter
        #     # Secara langsung ini tidak mudah karena canvas Tkinter tidak langsung mengekspos pixel data.
        #     # Cara termudah biasanya adalah menyimpan sebagai Postscript, lalu mengkonversinya.

        #     # Contoh: Menyimpan sebagai Postscript (format vektor)
        #     file_path = "gambar_paint.ps"
        #     self.drawing_canvas.canvas.postscript(file=file_path, colormode='color')
        #     print(f"Gambar disimpan sebagai {file_path}. Perlu konversi ke JPG/PNG.")

        #     # Untuk mengkonversi ke PNG/JPG membutuhkan Ghostscript atau cara lain untuk rasterisasi PS
        #     # Image.open(file_path).save("gambar_paint.png", "PNG")
        #     # print("Gambar berhasil dikonversi ke gambar_paint.png")

        # except ImportError:
        #     print("Pillow tidak terinstal. Tidak dapat menyimpan gambar.")
        #     print("Untuk menyimpan gambar, instal Pillow: pip install Pillow")
        # except Exception as e:
        #     print(f"Gagal menyimpan gambar: {e}")
