# ui/widgets.py

import tkinter as tk
from tkinter import ttk

# Anda dapat menambahkan widget UI kustom di sini yang tidak umum.
# Contoh: Sebuah tombol dengan ikon yang lebih kompleks, atau slider dengan label khusus.


class IconToggleButton(tk.Button):
    """
    Tombol yang dapat beralih keadaan (misalnya, untuk alat aktif)
    dan menampilkan ikon.
    """

    def __init__(self, parent, icon_path, command=None, *args, **kwargs):
        # Ikon harus dimuat sebagai PhotoImage Tkinter
        # from PIL import Image, ImageTk # Jika menggunakan gambar
        # self.icon_image = ImageTk.PhotoImage(Image.open(icon_path))

        super().__init__(parent, *args, **kwargs)  # image=self.icon_image,

        self.command = command
        self.is_active = False
        self.config(relief=tk.RAISED, bd=2)  # Default relief

        if command:
            self.config(command=self._toggle_command)

    def _toggle_command(self):
        # Aksi untuk tombol
        if self.command:
            self.command()
        self.toggle_active()

    def toggle_active(self):
        """
        Mengubah keadaan aktif tombol.
        """
        self.is_active = not self.is_active
        if self.is_active:
            self.config(relief=tk.SUNKEN, bd=2)
        else:
            self.config(relief=tk.RAISED, bd=2)

    def set_active(self, active: bool):
        """
        Mengatur keadaan aktif tombol secara eksplisit.
        """
        self.is_active = active
        if self.is_active:
            self.config(relief=tk.SUNKEN, bd=2)
        else:
            self.config(relief=tk.RAISED, bd=2)

# Contoh penggunaan (akan diintegrasikan ke dalam toolbar nanti):
# icon_brush = IconToggleButton(parent_frame, "resources/icons/brush.png", command=lambda: app.set_tool("brush"))
# icon_brush.pack(side=tk.LEFT)


class LabeledSlider(tk.Frame):
    """
    Slider dengan label nilai yang selalu terlihat.
    """

    def __init__(self, parent, label_text: str, from_: int, to: int, initial_value: int, command=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = tk.Label(self, text=label_text)
        self.label.pack(side=tk.LEFT, padx=2)

        self.value_label = tk.Label(self, text=str(initial_value))
        self.value_label.pack(side=tk.RIGHT, padx=2)

        self.slider = ttk.Scale(
            self,
            from_=from_,
            to=to,
            orient=tk.HORIZONTAL,
            command=self._on_slider_change
        )
        self.slider.set(initial_value)
        self.slider.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        self._command = command

    def _on_slider_change(self, value):
        val = int(float(value))
        self.value_label.config(text=str(val))
        if self._command:
            self._command(val)

    def set_value(self, value: int):
        self.slider.set(value)
        self.value_label.config(text=str(int(value)))

    def get_value(self) -> int:
        return int(self.slider.get())

# Anda dapat menambahkan widget kustom lainnya di sini
# Misalnya, ColorSwatch (jika tidak hanya menggunakan Canvas sederhana)
# LayerListItem, ScrollableFrame, dll.
