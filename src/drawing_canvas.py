# src/drawing_canvas.py

import tkinter as tk


class DrawingCanvas(tk.Canvas):
    """
    Widget kanvas kustom untuk aplikasi menggambar.
    Menangani event mouse dan logika menggambar.
    """

    def __init__(self, master, current_color, brush_size, **kwargs):
        """
        Inisialisasi DrawingCanvas.

        Args:
            master (tk.Widget): Widget induk (misalnya tk.Tk atau tk.Frame).
            current_color (str): Warna kuas awal.
            brush_size (int): Ukuran kuas awal.
            **kwargs: Argumen tambahan untuk tk.Canvas (misalnya bg, height, width).
        """
        super().__init__(master, **kwargs)

        self.last_x, self.last_y = None, None
        self.current_color = current_color
        self.brush_size = brush_size
        self.is_eraser_mode = False
        # Dapatkan warna latar belakang kanvas
        self.canvas_bg_color = kwargs.get('bg', 'white')

        # Bind event mouse
        # Saat tombol mouse kiri ditekan
        self.bind("<Button-1>", self._start_draw)
        # Saat tombol mouse kiri ditahan dan digerakkan
        self.bind("<B1-Motion>", self._draw_line)
        # Saat tombol mouse kiri dilepas
        self.bind("<ButtonRelease-1>", self._stop_draw)

    def _start_draw(self, event):
        """
        Memulai proses menggambar saat mouse ditekan.
        """
        self.last_x, self.last_y = event.x, event.y

    def _draw_line(self, event):
        """
        Menggambar garis saat mouse digerakkan sambil ditahan.
        """
        if self.last_x is not None and self.last_y is not None:
            if self.is_eraser_mode:
                # Mode penghapus: menggambar dengan warna latar belakang kanvas
                draw_color = self.canvas_bg_color
            else:
                # Mode pensil: menggambar dengan warna kuas yang dipilih
                draw_color = self.current_color

            # Membuat garis pada kanvas
            self.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=draw_color,
                width=self.brush_size,
                capstyle=tk.ROUND,    # Bentuk ujung garis bulat
                smooth=tk.TRUE        # Membuat garis lebih halus
            )
            self.last_x, self.last_y = event.x, event.y

    def _stop_draw(self, event):
        """
        Menghentikan proses menggambar saat mouse dilepas.
        """
        self.last_x, self.last_y = None, None

    def set_color(self, color):
        """
        Mengatur warna kuas yang digunakan untuk menggambar.

        Args:
            color (str): Kode warna (misalnya "red", "#RRGGBB").
        """
        self.current_color = color
        # Jika sedang dalam mode penghapus dan ingin kembali ke mode pensil,
        # pastikan warna kuas diperbarui.
        if not self.is_eraser_mode:
            # Mengembalikan cursor ke mode menggambar
            self.config(cursor=f'hand2')

    def set_brush_size(self, size):
        """
        Mengatur ukuran kuas.

        Args:
            size (int): Ukuran kuas dalam piksel.
        """
        self.brush_size = size

    def toggle_eraser(self, mode):
        """
        Mengaktifkan atau menonaktifkan mode penghapus.

        Args:
            mode (bool): True untuk mode penghapus, False untuk mode pensil.
        """
        self.is_eraser_mode = mode
        if self.is_eraser_mode:
            # Cursor dot untuk penghapus
            self.config(cursor=f'dot {self.brush_size + 5}')
        else:
            self.config(cursor=f'hand2')  # Cursor tangan untuk menggambar

    def clear_canvas(self):
        """
        Menghapus semua objek yang digambar dari kanvas.
        """
        self.delete("all")
