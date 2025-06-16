# core/canvas_manager.py
# Made by ade7

import tkinter as tk
from PIL import Image, ImageDraw, ImageTk  # Import wajib Pillow (PIL)
import io

# Import dari config
from config import AppConfig

# Import dari drawing_tools
from core.drawing_tools import BrushTool, EraserTool, LineTool, RectangleTool


class CanvasManager:
    """
    Mengelola kanvas gambar dan semua operasi terkait menggambar,
    serta riwayat undo/redo.
    """

    def __init__(self, app_instance, parent_frame: tk.Frame):
        """
        Inisialisasi manajer kanvas.

        Args:
            app_instance: Instance dari kelas Application.
            parent_frame (tk.Frame): Frame Tkinter tempat kanvas akan ditempatkan.
        """
        self.app = app_instance
        self.parent_frame = parent_frame
        self.canvas = None  # Objek tk.Canvas

        # Objek PIL Image, mewakili keadaan kanvas utama (komposit layer)
        self.current_image = None
        self.drawing_context = None  # Objek PIL ImageDraw untuk menggambar ke current_image

        self.undo_history = []
        self.redo_history = []
        self.history_limit = AppConfig.MAX_UNDO_HISTORY

        self._create_canvas()
        # Initialisasi image PIL akan dilakukan di Application setelah LayerManager dibuat
        # self._initialize_image() # Ini akan diganti oleh layer_manager.get_composite_image()
        self._bind_events()

        # Digunakan untuk menggambar garis continue
        self.last_x, self.last_y = None, None
        # Alat gambar aktif (misal: BrushTool, LineTool)
        self.current_drawing_tool = None

        print("CanvasManager diinisialisasi.")

    def _create_canvas(self):
        """
        Membuat widget Tkinter Canvas.
        """
        self.canvas = tk.Canvas(
            self.parent_frame,
            bg=AppConfig.DEFAULT_BACKGROUND_COLOR,
            width=AppConfig.DEFAULT_CANVAS_WIDTH,
            height=AppConfig.DEFAULT_CANVAS_HEIGHT,
            bd=0,  # Tanpa border
            highlightthickness=0  # Tanpa highlight border saat fokus
        )
        self.canvas.pack(expand=True, fill="both", padx=10, pady=10)
        # Made by ade7: Canvas utama aplikasi
        print("Tkinter Canvas dibuat.")

    def _initialize_image(self):
        """
        Menginisialisasi objek PIL Image kosong yang akan dirender ke kanvas.
        Ini sekarang dipanggil oleh Application setelah LayerManager siap.
        """
        # Ini sekarang akan mengambil gambar komposit dari LayerManager
        self.current_image = self.app.layer_manager.get_composite_image()
        if self.current_image:
            self.drawing_context = ImageDraw.Draw(self.current_image)
            self._update_canvas_display()
            print("Objek PIL Image diinisialisasi dari LayerManager.")
        else:
            print("Tidak dapat menginisialisasi gambar utama, LayerManager belum siap.")

    def _bind_events(self):
        """
        Mengikat event mouse ke kanvas.
        """
        self.canvas.bind("<Button-1>", self._on_mouse_down)
        self.canvas.bind("<B1-Motion>", self._on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
        # Event untuk resize kanvas
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        print("Event mouse terikat ke kanvas.")

    def _on_canvas_configure(self, event):
        """
        Menangani event ketika ukuran kanvas berubah.
        Akan menyesuaikan ukuran gambar PIL agar sesuai dengan kanvas.
        Ini akan mempengaruhi ukuran layer juga.
        """
        new_width = event.width
        new_height = event.height

        if new_width <= 1 or new_height <= 1:
            return  # Hindari ukuran tidak valid

        # Update ukuran layer di LayerManager
        self.app.layer_manager.canvas_width = new_width
        self.app.layer_manager.canvas_height = new_height
        # Perbarui ukuran setiap layer jika perlu
        for layer in self.app.layer_manager.layers:
            if layer.image and (layer.image.width != new_width or layer.image.height != new_height):
                old_image = layer.image
                # Buat layer baru transparan
                layer.image = Image.new(
                    "RGBA", (new_width, new_height), (0, 0, 0, 0))
                # Salin konten lama ke tengah layer baru
                x_offset = (new_width - old_image.width) // 2
                y_offset = (new_height - old_image.height) // 2
                layer.image.paste(
                    old_image, (max(0, x_offset), max(0, y_offset)))
                layer.draw_context = ImageDraw.Draw(
                    layer.image)  # Perbarui drawing context layer

        # Perbarui gambar utama komposit dan konteks gambar
        self.current_image = self.app.layer_manager.get_composite_image()
        if self.current_image:
            self.drawing_context = ImageDraw.Draw(self.current_image)
            self._update_canvas_display()
            print(
                f"Kanvas dan layer diubah ukurannya ke: {new_width}x{new_height}")

    def _on_mouse_down(self, event):
        """
        Menangani event mouse button down.
        """
        if self.app.current_tool in ["brush", "eraser", "line", "rectangle"]:
            # Simpan keadaan sebelum menggambar
            self._add_to_history()

            # Pilih alat yang sesuai
            active_layer = self.app.layer_manager.get_active_layer()
            if not active_layer:
                print("Tidak ada layer aktif untuk menggambar.")
                return

            if self.app.current_tool == "brush":
                self.current_drawing_tool = BrushTool(
                    active_layer.draw_context, self.app.current_color, self.app.current_brush_size)
            elif self.app.current_tool == "eraser":
                self.current_drawing_tool = EraserTool(
                    active_layer.draw_context, AppConfig.DEFAULT_BACKGROUND_COLOR, self.app.current_brush_size)
            elif self.app.current_tool == "line":
                self.current_drawing_tool = LineTool(
                    active_layer.draw_context, self.app.current_color, self.app.current_brush_size)
                # Untuk alat bentuk, kita juga perlu referensi ke canvas Tkinter untuk pratinjau
                self.current_drawing_tool.canvas_tk = self.canvas  # Meneruskan canvas Tkinter
            elif self.app.current_tool == "rectangle":
                self.current_drawing_tool = RectangleTool(
                    active_layer.draw_context, self.app.current_color, self.app.current_brush_size)
                self.current_drawing_tool.canvas_tk = self.canvas  # Meneruskan canvas Tkinter

            if self.current_drawing_tool:
                self.current_drawing_tool.start_draw(event.x, event.y)
                self.last_x, self.last_y = event.x, event.y
        elif self.app.current_tool == "text":
            # Text tool memiliki logikanya sendiri di TextTool class
            pass
        elif self.app.current_tool == "selection":
            # Selection tool memiliki logikanya sendiri di SelectionTool class
            pass

    def _on_mouse_drag(self, event):
        """
        Menangani event mouse drag (gerakan mouse saat tombol ditekan).
        """
        if self.current_drawing_tool and self.app.current_tool in ["brush", "eraser"]:
            self.current_drawing_tool.draw(
                self.last_x, self.last_y, event.x, event.y)
            self.last_x, self.last_y = event.x, event.y
            # Setelah menggambar ke layer aktif, perbarui gambar komposit utama
            self.current_image = self.app.layer_manager.get_composite_image()
            self.drawing_context = ImageDraw.Draw(
                self.current_image)  # Perbarui konteks gambar utama
            self._update_canvas_display()
        elif self.current_drawing_tool and self.app.current_tool in ["line", "rectangle"]:
            # Untuk alat bentuk, hanya perbarui pratinjau di canvas Tkinter
            self.current_drawing_tool.draw(
                self.last_x, self.last_y, event.x, event.y)
            # Tidak perlu update current_image di sini karena hanya pratinjau
            # Ini untuk memastikan gambar PIL tetap di bawah pratinjau Tkinter
            self._update_canvas_display()

    def _on_mouse_up(self, event):
        """
        Menangani event mouse button release.
        """
        if self.current_drawing_tool and self.app.current_tool in ["line", "rectangle"]:
            # Gambar bentuk final ke layer aktif
            active_layer = self.app.layer_manager.get_active_layer()
            if active_layer:
                # Pastikan konteks gambar ke layer aktif
                self.current_drawing_tool.drawing_context = active_layer.draw_context
                self.current_drawing_tool.end_draw(event.x, event.y)
                # Setelah menggambar ke layer aktif, perbarui gambar komposit utama
                self.current_image = self.app.layer_manager.get_composite_image()
                self.drawing_context = ImageDraw.Draw(
                    self.current_image)  # Perbarui konteks gambar utama
                self._update_canvas_display()  # Perbaikan: Panggil dari self

        self.last_x, self.last_y = None, None
        self.current_drawing_tool = None
        print("Mouse dilepas.")

    def _update_canvas_display(self):
        """
        Memperbarui tampilan kanvas Tkinter dengan gambar komposit saat ini.
        """
        if self.current_image:
            # Pastikan gambar sesuai dengan ukuran kanvas untuk ditampilkan dengan benar
            display_image = self.current_image.copy()

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            if canvas_width > 0 and canvas_height > 0 and \
               (display_image.width != canvas_width or display_image.height != canvas_height):
                # Resize hanya untuk tampilan, bukan mengubah data gambar asli dari layer
                display_image = display_image.resize(
                    (canvas_width, canvas_height), Image.Resampling.LANCZOS
                )

            self.tk_image = ImageTk.PhotoImage(display_image)
            # Hapus semua item gambar di Tkinter Canvas
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)
        else:
            # Pastikan kanvas kosong jika tidak ada gambar
            self.canvas.delete("all")

    def _add_to_history(self):
        """
        Menyimpan keadaan gambar komposit saat ini ke riwayat undo.
        """
        composite_img = self.app.layer_manager.get_composite_image()
        if composite_img:
            # Simpan salinan gambar komposit saat ini
            img_copy = composite_img.copy()

            # Jika riwayat undo melebihi batas, hapus yang tertua
            if len(self.undo_history) >= self.history_limit:
                self.undo_history.pop(0)

            self.undo_history.append(img_copy)
            self.redo_history.clear()  # Hapus riwayat redo setiap kali ada operasi baru
            print(
                f"Keadaan kanvas ditambahkan ke riwayat undo. Panjang: {len(self.undo_history)}")

    def undo(self):
        """
        Mengembalikan keadaan kanvas ke langkah sebelumnya.
        """
        if len(self.undo_history) > 1:  # Perlu setidaknya 2 item untuk undo (saat ini dan sebelumnya)
            # Pindahkan keadaan saat ini ke riwayat redo
            current_state_to_redo = self.undo_history.pop()
            self.redo_history.append(current_state_to_redo)

            # Ambil keadaan sebelumnya dari riwayat undo
            previous_image = self.undo_history[-1]

            # Buat layer manager untuk mengembalikan state
            # Ini adalah bagian yang kompleks dengan layer,
            # untuk kesederhanaan, kita akan mengganti gambar komposit utama.
            # Implementasi undo layer per layer akan lebih kompleks.
            self.current_image = previous_image.copy()
            self.drawing_context = ImageDraw.Draw(self.current_image)
            self._update_canvas_display()
            print("Undo berhasil.")
            self.app.main_window.update_status("Undo.")
        else:
            print("Tidak ada yang bisa di-undo.")
            self.app.main_window.update_status("Tidak ada yang bisa di-undo.")

    def redo(self):
        """
        Menerapkan kembali keadaan kanvas dari riwayat redo.
        """
        if self.redo_history:
            # Pindahkan keadaan dari redo ke undo
            next_image = self.redo_history.pop()
            self.undo_history.append(next_image)

            self.current_image = next_image.copy()
            self.drawing_context = ImageDraw.Draw(self.current_image)
            self._update_canvas_display()
            print("Redo berhasil.")
            self.app.main_window.update_status("Redo.")
        else:
            print("Tidak ada yang bisa di-redo.")
            self.app.main_window.update_status("Tidak ada yang bisa di-redo.")

    def clear_canvas(self):
        """
        Membersihkan kanvas sepenuhnya.
        (Ini sekarang akan membersihkan layer aktif, logikanya dipindahkan ke Application)
        """
        pass  # Logika dipindahkan ke app.clear_canvas()

    def save_image(self, file_path: str, image_to_save=None):
        """
        Menyimpan gambar kanvas saat ini (atau gambar yang ditentukan) ke file.
        """
        if image_to_save is None:
            image_to_save = self.current_image  # Default adalah gambar komposit

        if image_to_save:
            try:
                # PIL akan secara otomatis mengonversi RGBA ke format output yang sesuai
                # saat menyimpan ke PNG/JPG.
                image_to_save.save(file_path)
                print(f"Gambar berhasil disimpan ke: {file_path}")
            except Exception as e:
                print(f"Gagal menyimpan gambar: {e}")
        else:
            print("Tidak ada gambar untuk disimpan.")

    def open_image(self, file_path: str):
        """
        Membuka gambar dari file dan menampilkannya di kanvas.
        (Logikanya dipindahkan ke Application untuk integrasi LayerManager)
        """
        pass  # Logika dipindahkan ke app.open_image()
