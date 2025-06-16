# core/application.py

from features.layer_manager import Layer, LayerManager  # Import Layer juga
from features.filters import ImageFilters
from features.selection_tool import SelectionTool
from features.text_tool import TextTool
from ui.menus import MainMenu
from ui.toolbars import ToolbarPanel
from ui.main_window import MainWindow
from core.canvas_manager import CanvasManager
from config import AppConfig
import tkinter as tk
import sys
import os
import time  # Import modul time untuk mengukur durasi
# Pastikan ImageDraw terimpor di sini juga untuk konteks drawing
from PIL import ImageDraw

# Pastikan direktori induk (complex-paint-app/) ada di path
# agar modul dari config, ui, features, dan utils dapat diimpor.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class Application:
    """
    Kelas utama aplikasi Paint, mengelola jendela utama dan koordinasi komponen.
    """

    def __init__(self, root: tk.Tk):
        """
        Inisialisasi aplikasi.

        Args:
            root (tk.Tk): Objek Tkinter root window.
        """
        self.root = root
        self.root.title(AppConfig.WINDOW_TITLE)
        self.root.geometry(
            f"{AppConfig.DEFAULT_WINDOW_WIDTH}x{AppConfig.DEFAULT_WINDOW_HEIGHT}")

        # Alat aktif saat ini (misal: "brush", "eraser", "pencil", "text", "line", "rectangle")
        self.current_tool = "brush"
        self.current_brush_size = AppConfig.DEFAULT_BRUSH_SIZE
        self.current_color = AppConfig.DEFAULT_BRUSH_COLOR

        # --- Inisialisasi Komponen ---
        start_time_ui_init = time.time()  # Mulai pengukuran UI utama

        # Inisialisasi jendela utama (akan menampilkan loading screen)
        self.main_window = MainWindow(self.root, self)

        # Inisialisasi manajer layer (sebelum canvas_manager agar canvas_manager bisa menggunakannya)
        self.layer_manager = LayerManager(
            self, AppConfig.DEFAULT_CANVAS_WIDTH, AppConfig.DEFAULT_CANVAS_HEIGHT)

        # Inisialisasi manajer kanvas, meneruskan frame kanvas dari main_window
        self.canvas_manager = CanvasManager(
            self, self.main_window.canvas_frame)
        # Atur current_image dari canvas_manager untuk sinkronisasi awal
        self.canvas_manager.current_image = self.layer_manager.get_composite_image()
        self.canvas_manager._update_canvas_display()  # Perbarui tampilan awal kanvas

        # Inisialisasi menu dan toolbar
        self.main_menu = MainMenu(self.root, self)
        self.toolbar_panel = ToolbarPanel(self.main_window.top_frame, self)

        # Inisialisasi alat fitur
        self.text_tool = TextTool(self.canvas_manager, self)
        self.selection_tool = SelectionTool(self.canvas_manager)
        self.image_filters = ImageFilters(self)

        # Mengupdate tampilan UI awal
        self.toolbar_panel.update_ui_elements()

        end_time_ui_init = time.time()  # Akhiri pengukuran UI utama
        print(
            f"DEBUG: Inisialisasi UI dan fitur selesai dalam {end_time_ui_init - start_time_ui_init:.4f} detik.")
        print("Application diinisialisasi sepenuhnya.")

    def run(self):
        """
        Memulai event loop Tkinter.
        """
        # self.root.deiconify() # Tampilkan jendela utama setelah inisialisasi selesai
        self.root.mainloop()

    def set_tool(self, tool_name: str):
        """
        Mengatur alat gambar yang aktif dan mengelola aktivasi/deaktivasi alat.
        """
        # Deaktivasi alat yang sedang aktif jika ada
        if self.current_tool == "text" and self.text_tool:
            self.text_tool.deactivate()
        elif self.current_tool == "selection" and self.selection_tool:
            self.selection_tool.deactivate()
        # Tambahkan kondisi untuk alat lain yang memerlukan aktivasi/deaktivasi eksplisit

        self.current_tool = tool_name
        self.main_window.update_status(
            f"Alat diatur ke: {self.current_tool.capitalize()}")
        print(f"Alat diatur ke: {self.current_tool}")
        self.toolbar_panel.update_ui_elements()  # Perbarui visual tombol alat

        # Aktivasi alat yang baru dipilih
        if self.current_tool == "text" and self.text_tool:
            self.text_tool.activate()
        elif self.current_tool == "selection" and self.selection_tool:
            self.selection_tool.activate()

    def set_brush_size(self, size: int):
        """
        Mengatur ukuran kuas.
        """
        self.current_brush_size = max(
            AppConfig.MIN_BRUSH_SIZE, min(size, AppConfig.MAX_BRUSH_SIZE))
        self.main_window.update_status(
            f"Ukuran kuas: {self.current_brush_size} px")
        print(f"Ukuran kuas diatur ke: {self.current_brush_size}")
        # Logika untuk memperbarui UI slider/label di sini sudah ada di ToolbarPanel

    def set_color(self, hex_color: str):
        """
        Mengatur warna gambar.
        """
        self.current_color = hex_color
        self.main_window.update_status(
            f"Warna diatur ke: {self.current_color}")
        print(f"Warna diatur ke: {self.current_color}")
        self.toolbar_panel.update_ui_elements()  # Perbarui swatch warna

    def clear_canvas(self):
        """
        Membersihkan kanvas gambar.
        """
        # Hapus konten layer aktif
        active_layer = self.layer_manager.get_active_layer()
        if active_layer:
            self.canvas_manager._add_to_history()  # Simpan keadaan sebelum dibersihkan
            active_layer.clear()
            self.canvas_manager.current_image = self.layer_manager.get_composite_image()
            self.canvas_manager.drawing_context = ImageDraw.Draw(
                self.canvas_manager.current_image)  # Perbarui konteks gambar
            self.canvas_manager._update_canvas_display()
            self.main_window.update_status("Kanvas aktif dibersihkan.")
            print("Kanvas aktif dibersihkan.")
        else:
            print("Tidak ada layer aktif untuk dibersihkan.")
            self.main_window.update_status("Tidak ada layer aktif.")

    def undo(self):
        """
        Melakukan operasi undo.
        """
        self.canvas_manager.undo()
        self.main_window.update_status("Undo dilakukan.")

    def redo(self):
        """
        Melakukan operasi redo.
        """
        self.canvas_manager.redo()
        self.main_window.update_status("Redo dilakukan.")

    def save_image(self, file_path: str):
        """
        Menyimpan gambar komposit ke file.
        """
        composite_image = self.layer_manager.get_composite_image()
        if composite_image:
            # Meneruskan gambar komposit
            self.canvas_manager.save_image(
                file_path, image_to_save=composite_image)
        else:
            self.main_window.update_status("Tidak ada gambar untuk disimpan.")
            print("Tidak ada gambar komposit untuk disimpan.")

    def open_image(self, file_path: str):
        """
        Membuka gambar dari file dan menampilkannya di kanvas (pada layer baru).
        """
        # self.canvas_manager.open_image(file_path) # Ini akan diganti untuk layer

        # Contoh: Buat layer baru dan muat gambar ke layer itu
        print(f"Membuka gambar dari: {file_path}. (Akan dimuat ke layer baru)")
        self.main_window.update_status(
            f"Membuka: {os.path.basename(file_path)} ke layer baru.")
        try:
            from PIL import Image, ImageDraw
            img = Image.open(file_path).convert(
                "RGBA")  # Pastikan RGBA untuk layer

            # Buat layer baru
            new_layer_name = os.path.basename(file_path).split('.')[0]
            new_layer = Layer(self.canvas_manager.canvas.winfo_width(
            ), self.canvas_manager.canvas.winfo_height(), name=new_layer_name)

            # Posisikan gambar di tengah layer baru
            x_offset = (new_layer.image.width - img.width) // 2
            y_offset = (new_layer.image.height - img.height) // 2
            # Gunakan mask untuk transparansi
            new_layer.image.paste(img, (x_offset, y_offset), img)

            self.layer_manager.add_layer(name=new_layer_name)
            # Ganti layer placeholder dengan yang baru dibuat
            self.layer_manager.layers[-1] = new_layer
            self.layer_manager.set_active_layer(
                len(self.layer_manager.layers) - 1)

            # Perbarui kanvas dengan gambar komposit baru
            self.canvas_manager.current_image = self.layer_manager.get_composite_image()
            self.canvas_manager.drawing_context = ImageDraw.Draw(
                self.canvas_manager.current_image)
            self.canvas_manager._update_canvas_display()
            # Tambahkan keadaan setelah membuka gambar ke history
            self.canvas_manager._add_to_history()
            print(
                f"Gambar '{os.path.basename(file_path)}' berhasil dimuat ke layer baru.")
        except Exception as e:
            print(f"Gagal membuka gambar ke layer baru: {e}")
            self.main_window.update_status(f"Gagal membuka gambar: {e}")

    def apply_filter(self, filter_name: str, **kwargs):
        """Menerapkan filter ke layer aktif."""
        active_layer = self.layer_manager.get_active_layer()
        if active_layer and active_layer.image:
            self.canvas_manager._add_to_history()  # Simpan keadaan sebelum filter

            try:
                from PIL import Image, ImageFilter, ImageOps, ImageEnhance
                processed_image = active_layer.image.copy()

                if filter_name == "grayscale":
                    processed_image = ImageOps.grayscale(processed_image)
                elif filter_name == "sepia":
                    pixels = processed_image.load()
                    for i in range(processed_image.size[0]):
                        for j in range(processed_image.size[1]):
                            r, g, b, a = pixels[i, j]  # Ambil juga alpha
                            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                            pixels[i, j] = (min(255, tr), min(255, tg), min(
                                255, tb), a)  # Pertahankan alpha
                elif filter_name == "blur":
                    radius = kwargs.get("radius", 2)
                    processed_image = processed_image.filter(
                        ImageFilter.GaussianBlur(radius))
                elif filter_name == "sharpen":
                    processed_image = processed_image.filter(
                        ImageFilter.SHARPEN)
                elif filter_name == "invert":
                    processed_image = ImageOps.invert(processed_image.convert("RGB")).convert(
                        "RGBA")  # Invert RGB lalu konversi kembali ke RGBA
                elif filter_name == "brightness":
                    factor = kwargs.get("factor", 1.2)
                    enhancer = ImageEnhance.Brightness(processed_image)
                    processed_image = enhancer.enhance(factor)
                elif filter_name == "contrast":
                    factor = kwargs.get("factor", 1.2)
                    enhancer = ImageEnhance.Contrast(processed_image)
                    processed_image = enhancer.enhance(factor)
                else:
                    print(f"Filter '{filter_name}' tidak dikenal.")
                    self.main_window.update_status(
                        f"Filter '{filter_name}' tidak dikenal.")
                    self.canvas_manager.undo_history.pop()  # Hapus dari history
                    return

                active_layer.image = processed_image
                active_layer.draw_context = ImageDraw.Draw(
                    active_layer.image)  # Perbarui drawing context layer
                # Update gambar kanvas utama
                self.canvas_manager.current_image = self.layer_manager.get_composite_image()
                self.canvas_manager.drawing_context = ImageDraw.Draw(
                    self.canvas_manager.current_image)  # Perbarui konteks gambar utama
                self.canvas_manager._update_canvas_display()
                self.main_window.update_status(
                    f"Filter '{filter_name}' diterapkan ke layer aktif.")

            except ImportError:
                print("Pillow (PIL) tidak terinstal. Filter dibatalkan.")
                self.main_window.update_status(
                    "Pillow tidak terinstal. Filter dibatalkan.")
                self.canvas_manager.undo_history.pop()
            except Exception as e:
                print(f"Error menerapkan filter: {e}")
                self.main_window.update_status(f"Error filter: {e}")
                self.canvas_manager.undo_history.pop()
        else:
            print("Tidak ada layer aktif atau gambar di layer aktif.")
            self.main_window.update_status(
                "Tidak ada layer aktif untuk filter.")
