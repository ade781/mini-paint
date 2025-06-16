# ui/toolbars.py

import tkinter as tk
from tkinter import ttk  # Untuk widget yang lebih modern seperti Scale

# Import dari config
from config import AppConfig

# Import dari utilitas warna
from utils.color_utils import hex_to_rgb  # Untuk pratinjau warna


class ToolbarPanel:
    """
    Mengelola panel toolbar utama di bagian atas jendela aplikasi.
    """

    def __init__(self, parent_frame: tk.Frame, app_instance):
        """
        Inisialisasi panel toolbar.

        Args:
            parent_frame (tk.Frame): Frame Tkinter tempat toolbar akan ditempatkan.
            app_instance: Instance dari kelas Application.
        """
        self.parent_frame = parent_frame
        self.app = app_instance

        self._create_tool_toolbar()
        self._create_brush_toolbar()
        self._create_color_toolbar()
        self._create_action_toolbar()  # Untuk undo/redo/clear/save

        self.update_ui_elements()  # Memastikan UI mencerminkan keadaan aplikasi saat ini
        print("ToolbarPanel diinisialisasi.")

    def _create_tool_toolbar(self):
        """
        Membuat toolbar untuk pemilihan alat gambar.
        """
        tool_frame = tk.LabelFrame(
            self.parent_frame, text="Tools", padx=5, pady=5)
        tool_frame.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.Y)

        self.tool_buttons = {}  # Untuk menyimpan referensi tombol alat

        brush_button = tk.Button(
            tool_frame, text="Brush", command=lambda: self.app.set_tool("brush"))
        brush_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.tool_buttons["brush"] = brush_button

        eraser_button = tk.Button(
            tool_frame, text="Eraser", command=lambda: self.app.set_tool("eraser"))
        eraser_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.tool_buttons["eraser"] = eraser_button

        line_button = tk.Button(tool_frame, text="Line",
                                command=lambda: self.app.set_tool("line"))
        line_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.tool_buttons["line"] = line_button

        rect_button = tk.Button(
            tool_frame, text="Rectangle", command=lambda: self.app.set_tool("rectangle"))
        rect_button.pack(side=tk.LEFT, padx=2, pady=2)
        self.tool_buttons["rectangle"] = rect_button

        # Tambahkan lebih banyak tombol alat di sini
        print("Toolbar alat dibuat.")

    def _create_brush_toolbar(self):
        """
        Membuat toolbar untuk ukuran kuas.
        """
        brush_frame = tk.LabelFrame(
            self.parent_frame, text="Brush Size", padx=5, pady=5)
        brush_frame.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.Y)

        self.brush_size_slider = ttk.Scale(
            brush_frame,
            from_=AppConfig.MIN_BRUSH_SIZE,
            to=AppConfig.MAX_BRUSH_SIZE,
            orient=tk.HORIZONTAL,
            command=self._on_brush_size_change
        )
        self.brush_size_slider.set(
            self.app.current_brush_size)  # Set nilai awal
        self.brush_size_slider.pack(side=tk.LEFT, padx=2, pady=2)

        self.brush_size_label = tk.Label(
            brush_frame, text=f"{self.app.current_brush_size} px")
        self.brush_size_label.pack(side=tk.LEFT, padx=2, pady=2)
        print("Toolbar ukuran kuas dibuat.")

    def _on_brush_size_change(self, value):
        """
        Callback saat slider ukuran kuas digeser.
        """
        size = int(float(value))
        self.app.set_brush_size(size)
        self.brush_size_label.config(text=f"{size} px")

    def _create_color_toolbar(self):
        """
        Membuat toolbar untuk pemilihan warna.
        """
        color_frame = tk.LabelFrame(
            self.parent_frame, text="Colors", padx=5, pady=5)
        color_frame.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.Y)

        # Tombol pemilih warna utama
        self.current_color_swatch = tk.Canvas(
            color_frame, width=24, height=24, bd=1, relief=tk.SUNKEN,
            bg=self.app.current_color  # Warna awal
        )
        self.current_color_swatch.pack(side=tk.LEFT, padx=2, pady=2)
        self.current_color_swatch.bind(
            "<Button-1>", lambda e: self.app.main_window.show_color_picker())

        # Palet warna cepat
        for color_hex in AppConfig.COLOR_PALETTE:
            swatch = tk.Canvas(color_frame, width=18, height=18,
                               bd=1, relief=tk.RIDGE, bg=color_hex)
            swatch.pack(side=tk.LEFT, padx=1, pady=1)
            swatch.bind("<Button-1>", lambda e,
                        c=color_hex: self.app.set_color(c))
        print("Toolbar warna dibuat.")

    def _create_action_toolbar(self):
        """
        Membuat toolbar untuk aksi-aksi umum (undo, redo, clear, save).
        """
        action_frame = tk.LabelFrame(
            self.parent_frame, text="Actions", padx=5, pady=5)
        action_frame.pack(side=tk.LEFT, padx=5, pady=2, fill=tk.Y)

        undo_button = tk.Button(
            action_frame, text="Undo", command=self.app.undo)
        undo_button.pack(side=tk.LEFT, padx=2, pady=2)

        redo_button = tk.Button(
            action_frame, text="Redo", command=self.app.redo)
        redo_button.pack(side=tk.LEFT, padx=2, pady=2)

        clear_button = tk.Button(
            action_frame, text="Clear", command=self.app.clear_canvas)
        clear_button.pack(side=tk.LEFT, padx=2, pady=2)

        save_button = tk.Button(action_frame, text="Save",
                                command=self.app.main_window.save_file)
        save_button.pack(side=tk.LEFT, padx=2, pady=2)
        print("Toolbar aksi dibuat.")

    def update_ui_elements(self):
        """
        Memperbarui elemen UI agar mencerminkan status aplikasi saat ini.
        Dipanggil setiap kali status aplikasi (alat, warna, ukuran) berubah.
        """
        # Update warna aktif di swatch
        self.current_color_swatch.config(bg=self.app.current_color)

        # Update ukuran kuas di slider dan label
        self.brush_size_slider.set(self.app.current_brush_size)
        self.brush_size_label.config(text=f"{self.app.current_brush_size} px")

        # Update tampilan tombol alat (misal, tambahkan border atau highlight)
        for tool, button in self.tool_buttons.items():
            if tool == self.app.current_tool:
                button.config(relief=tk.SUNKEN, bd=2)
            else:
                button.config(relief=tk.RAISED, bd=2)
        print("Elemen UI diperbarui.")
