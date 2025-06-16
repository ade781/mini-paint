# features/selection_tool.py

import tkinter as tk
# from PIL import Image, ImageDraw, ImageTk # Akan digunakan untuk manipulasi gambar

# Import dari core.drawing_tools untuk inheritance jika diperlukan
# from core.drawing_tools import BaseTool


class SelectionTool:  # Bisa juga mewarisi dari BaseTool jika ingin berinteraksi dengan CanvasManager
    """
    Mengelola alat seleksi, seperti seleksi persegi panjang atau lasso.
    """

    def __init__(self, canvas_manager):
        self.canvas_manager = canvas_manager
        self._start_x, self._start_y = None, None
        self._selection_rect_id = None  # Untuk menampilkan persegi panjang seleksi

    def activate(self):
        """
        Mengaktifkan alat seleksi.
        """
        print("Alat Seleksi diaktifkan.")
        self.canvas_manager.canvas.bind("<Button-1>", self._on_mouse_down)
        self.canvas_manager.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas_manager.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)

    def deactivate(self):
        """
        Menonaktifkan alat seleksi.
        """
        print("Alat Seleksi dinonaktifkan.")
        self.canvas_manager.canvas.unbind("<Button-1>")
        self.canvas_manager.canvas.unbind("<B1-Motion>")
        self.canvas_manager.canvas.unbind("<ButtonRelease-1>")
        self._clear_selection_visual()

    def _on_mouse_down(self, event):
        self._start_x, self._start_y = event.x, event.y
        self._clear_selection_visual()
        # Buat visualisasi seleksi awal
        self._selection_rect_id = self.canvas_manager.canvas.create_rectangle(
            self._start_x, self._start_y, event.x, event.y,
            outline="blue", dash=(5, 5)
        )

    def _on_mouse_drag(self, event):
        if self._selection_rect_id:
            self.canvas_manager.canvas.coords(
                self._selection_rect_id,
                self._start_x, self._start_y, event.x, event.y
            )

    def _on_mouse_up(self, event):
        if self._start_x is not None:
            x1, y1 = min(self._start_x, event.x), min(self._start_y, event.y)
            x2, y2 = max(self._start_x, event.x), max(self._start_y, event.y)
            self.current_selection = (x1, y1, x2, y2)
            print(f"Seleksi dibuat: {self.current_selection}")
            self._start_x, self._start_y = None, None
            # Biarkan visualisasi seleksi tetap ada sampai seleksi baru dimulai atau dibatalkan

    def _clear_selection_visual(self):
        """Menghapus visualisasi persegi panjang seleksi dari kanvas."""
        if self._selection_rect_id:
            self.canvas_manager.canvas.delete(self._selection_rect_id)
            self._selection_rect_id = None
            self.current_selection = None
            print("Visualisasi seleksi dihapus.")

    def get_selected_area(self):
        """
        Mengembalikan koordinat area yang terseleksi.
        """
        return self.current_selection

    def apply_to_selection(self, operation_func):
        """
        Menerapkan fungsi ke area yang terseleksi.
        operation_func akan menerima objek gambar (PIL Image) dan koordinat seleksi,
        dan mengembalikan gambar yang dimodifikasi.
        """
        if self.current_selection and self.canvas_manager.current_image:
            x1, y1, x2, y2 = self.current_selection

            try:
                from PIL import Image
                # Crop bagian yang terseleksi
                selected_region = self.canvas_manager.current_image.crop(
                    (x1, y1, x2, y2))

                # Terapkan operasi
                modified_region = operation_func(selected_region)

                # Paste kembali ke gambar utama
                self.canvas_manager.current_image.paste(
                    modified_region, (x1, y1))
                self.canvas_manager._update_canvas_display()
                self.canvas_manager._add_to_history()
                print("Operasi diterapkan ke area seleksi.")
            except ImportError:
                print(
                    "Pillow (PIL) tidak terinstal, tidak dapat menerapkan operasi ke seleksi.")
        else:
            print("Tidak ada area yang terseleksi atau gambar.")
