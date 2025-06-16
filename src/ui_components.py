# src/ui_components.py

import tkinter as tk
from tkinter import ttk


class UIComponents:
    """
    Kelas untuk membuat dan mengatur komponen UI (toolbar) aplikasi.
    """

    def __init__(self, master, on_color_pick, on_brush_size_change,
                 on_toggle_eraser, on_clear_canvas, on_save_image):
        """
        Inisialisasi komponen UI.

        Args:
            master (tk.Widget): Widget induk untuk toolbar.
            on_color_pick (callable): Fungsi yang dipanggil saat tombol warna diklik.
            on_brush_size_change (callable): Fungsi yang dipanggil saat slider ukuran kuas diubah.
            on_toggle_eraser (callable): Fungsi yang dipanggil saat tombol penghapus diklik.
            on_clear_canvas (callable): Fungsi yang dipanggil saat tombol bersihkan kanvas diklik.
            on_save_image (callable): Fungsi yang dipanggil saat tombol simpan gambar diklik.
        """
        self.master = master
        self.on_color_pick = on_color_pick
        self.on_brush_size_change = on_brush_size_change
        self.on_toggle_eraser = on_toggle_eraser
        self.on_clear_canvas = on_clear_canvas
        self.on_save_image = on_save_image

        self._create_toolbar()

    def _create_toolbar(self):
        """
        Membuat tombol-tombol dan slider untuk toolbar.
        """
        # Tombol Warna
        color_btn = ttk.Button(self.master, text="Warna",
                               command=self.on_color_pick)
        color_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Slider Ukuran Kuas
        ttk.Label(self.master, text="Ukuran Kuas:").pack(
            side=tk.LEFT, padx=(10, 2))
        self.brush_size_slider = ttk.Scale(
            self.master,
            from_=1, to=50,
            orient=tk.HORIZONTAL,
            command=self.on_brush_size_change
        )
        self.brush_size_slider.set(5)  # Set nilai awal slider
        self.brush_size_slider.pack(side=tk.LEFT, padx=5, pady=5)

        # Tombol Penghapus
        eraser_btn = ttk.Button(
            self.master, text="Penghapus", command=self.on_toggle_eraser)
        eraser_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Tombol Bersihkan Kanvas
        clear_btn = ttk.Button(
            self.master, text="Bersihkan", command=self.on_clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # Tombol Simpan Gambar
        save_btn = ttk.Button(self.master, text="Simpan",
                              command=self.on_save_image)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)
