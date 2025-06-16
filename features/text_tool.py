# features/text_tool.py

import tkinter as tk
from tkinter import simpledialog, font  # Untuk input teks dan pemilihan font

# from PIL import ImageFont, ImageDraw # Akan digunakan untuk menggambar teks ke gambar PIL


class TextTool:
    """
    Mengelola alat teks untuk menambahkan dan mengedit teks pada kanvas.
    """

    def __init__(self, canvas_manager, app_instance):
        self.canvas_manager = canvas_manager
        self.app = app_instance
        self._font_name = "Arial"
        self._font_size = 24
        self._font_weight = "normal"  # "normal" atau "bold"
        self._font_slant = "roman"  # "roman" atau "italic"

        self.active_text_entry = None  # Objek entry Tkinter sementara untuk input teks
        self.text_position_x, self.text_position_y = None, None

        print("TextTool diinisialisasi.")

    def activate(self):
        """
        Mengaktifkan alat teks. Menunggu klik untuk menempatkan teks.
        """
        print("Alat Teks diaktifkan. Klik pada kanvas untuk menempatkan teks.")
        self.canvas_manager.canvas.bind("<Button-1>", self._on_canvas_click)
        self.app.main_window.update_status(
            "Alat Teks aktif. Klik untuk menempatkan.")

    def deactivate(self):
        """
        Menonaktifkan alat teks.
        """
        print("Alat Teks dinonaktifkan.")
        self.canvas_manager.canvas.unbind("<Button-1>")
        self.app.main_window.update_status("Alat Teks tidak aktif.")
        if self.active_text_entry:
            self.active_text_entry.destroy()
            self.active_text_entry = None

    def _on_canvas_click(self, event):
        """
        Menangani klik pada kanvas untuk menempatkan input teks.
        """
        if self.active_text_entry:  # Jika sudah ada entry aktif, pindahkan
            self.active_text_entry.place(x=event.x, y=event.y, anchor="nw")
            self.text_position_x, self.text_position_y = event.x, event.y
            print(f"Memindahkan entry teks ke ({event.x}, {event.y})")
            return

        # Simpan posisi klik
        self.text_position_x, self.text_position_y = event.x, event.y

        # Buat entry teks sementara di kanvas
        self.active_text_entry = tk.Entry(self.canvas_manager.canvas,
                                          font=(self._font_name, self._font_size,
                                                self._font_weight, self._font_slant),
                                          fg=self.app.current_color,
                                          insertbackground=self.app.current_color,  # Warna kursor
                                          bd=1, relief=tk.SOLID)
        self.active_text_entry.place(x=event.x, y=event.y, anchor="nw")
        self.active_text_entry.focus_set()

        # Bind event untuk menekan Enter (menggambar teks) dan Escape (membatalkan)
        self.active_text_entry.bind("<Return>", self._draw_text_to_canvas)
        self.active_text_entry.bind("<Escape>", self._cancel_text_entry)
        print(f"Entry teks dibuat di ({event.x}, {event.y})")
        self.app.main_window.update_status(
            "Ketik teks, tekan Enter untuk menerapkan.")

    def _draw_text_to_canvas(self, event=None):
        """
        Menggambar teks dari entry ke gambar PIL pada kanvas.
        """
        text_to_draw = self.active_text_entry.get()
        if not text_to_draw:
            self._cancel_text_entry()
            return

        x, y = self.text_position_x, self.text_position_y
        color = self.app.current_color

        if self.canvas_manager.current_image and self.canvas_manager.drawing_context:
            try:
                from PIL import ImageFont, ImageDraw

                # Coba muat font kustom jika ada, jika tidak, gunakan font default PIL
                try:
                    # PIL membutuhkan path ke file font .ttf/.otf
                    # Anda mungkin perlu logika yang lebih canggih untuk menemukan font
                    # Untuk kesederhanaan, kita bisa asumsikan font ada di sistem atau mengabaikan pengaturan font
                    # Jika menggunakan font sistem, gunakan tk.font untuk mendapatkan nama font yang benar

                    # Font Tkinter dapat digunakan untuk mengukur teks, tetapi untuk menggambar di PIL Image
                    # kita perlu objek ImageFont dari PIL.ImageFont.truetype

                    # Untuk contoh ini, kita akan menggunakan font default PIL jika tidak ada file font spesifik
                    # atau font Arial/Times New Roman dari sistem jika PIL bisa menemukannya.

                    # Coba muat font dari nama
                    # font_path = ImageFont.get_path_from_system(self._font_name) # Tidak ada fungsi langsung seperti ini di PIL
                    # Solusi yang lebih baik adalah menggunakan ImageFont.truetype dengan jalur font yang diketahui

                    # Untuk demo, kita akan menggunakan font default yang dibangun di PIL
                    # atau fallback ke font sistem jika ImageFont.truetype menemukan namanya.
                    # Ini bisa jadi kompleks karena PIL mungkin tidak selalu menemukan font sistem hanya dengan nama.

                    # Pendekatan yang lebih andal untuk font sistem:
                    # Mencari file font berdasarkan nama atau menggunakan font default jika tidak ditemukan.
                    # Asumsikan 'arial.ttf' atau 'times.ttf' adalah font umum

                    try:
                        # Ini mungkin memerlukan instalasi font di sistem atau jalur ke file font
                        pil_font = ImageFont.truetype(
                            self._font_name + ".ttf", self._font_size)
                    except IOError:
                        # Fallback ke font default jika font spesifik tidak ditemukan
                        print(
                            f"Font '{self._font_name}.ttf' tidak ditemukan, menggunakan font default.")
                        pil_font = ImageFont.load_default()
                        # Sesuaikan ukuran jika menggunakan font default
                        # pil_font = ImageFont.truetype("arial.ttf", self._font_size) # Atau Arial jika tersedia
                        # Perlu cara lebih baik untuk menangani gaya font (bold/italic) dengan ImageFont.load_default()

                except Exception as e:
                    print(
                        f"Error memuat font: {e}. Menggunakan font default PIL.")
                    pil_font = ImageFont.load_default()

                self.canvas_manager._add_to_history()  # Simpan keadaan sebelum menggambar teks
                self.canvas_manager.drawing_context.text(
                    (x, y),
                    text_to_draw,
                    font=pil_font,
                    fill=color
                )
                self.canvas_manager._update_canvas_display()
                self.app.main_window.update_status("Teks diterapkan.")

            except ImportError:
                print("Pillow (PIL) tidak terinstal, tidak dapat menggambar teks.")
                self.app.main_window.update_status(
                    "Pillow tidak terinstal. Teks dibatalkan.")
            except Exception as e:
                print(f"Error menggambar teks: {e}")
                self.app.main_window.update_status(f"Error teks: {e}")

        self._cancel_text_entry()  # Hapus entry setelah teks diterapkan

    def _cancel_text_entry(self, event=None):
        """
        Membatalkan entri teks dan menghapus widget entry.
        """
        if self.active_text_entry:
            self.active_text_entry.destroy()
            self.active_text_entry = None
            self.text_position_x, self.text_position_y = None, None
            print("Entry teks dibatalkan.")
            self.app.main_window.update_status("Teks dibatalkan.")

    def set_font_properties(self, font_name: str = None, font_size: int = None, weight: str = None, slant: str = None):
        """
        Mengatur properti font untuk alat teks.
        """
        if font_name:
            self._font_name = font_name
        if font_size:
            self._font_size = font_size
        if weight:
            self._font_weight = weight
        if slant:
            self._font_slant = slant
        print(
            f"Properti font diatur: {self._font_name}, {self._font_size}, {self._font_weight}, {self._font_slant}")
        self.app.main_window.update_status("Properti font diperbarui.")

    def show_font_dialog(self):
        """
        Menampilkan dialog untuk memilih properti font.
        """
        # Anda bisa menggunakan simpledialog atau membuat dialog kustom yang lebih kompleks
        # Ini akan memerlukan dialog kustom atau impor dari ui.dialogs
        print("Menampilkan dialog pemilihan font. (Placeholder)")
        # Contoh:
        # font_info = self.app.main_window.show_font_properties_dialog(
        #     self._font_name, self._font_size, self._font_weight, self._font_slant
        # )
        # if font_info:
        #     self.set_font_properties(*font_info)
