# features/layer_manager.py

import tkinter as tk
from PIL import Image, ImageDraw  # Dipindahkan ke atas


class Layer:
    """
    Mewakili satu lapisan gambar.
    """

    # Menggunakan RGBA untuk transparansi
    def __init__(self, width: int, height: int, name: str = "Layer", background_color: str = "#00000000"):
        try:
            # from PIL import Image, ImageDraw # Impor sudah di atas
            # Default transparan penuh
            self.image = Image.new("RGBA", (width, height), background_color)
            self.draw_context = ImageDraw.Draw(self.image)
        except ImportError:
            print("Pillow (PIL) tidak terinstal. Layer tidak akan berfungsi penuh.")
            self.image = None
            self.draw_context = None

        self.name = name
        self.is_visible = True
        self.opacity = 1.0  # 0.0 (transparan) - 1.0 (buram)

    def set_visible(self, visible: bool):
        self.is_visible = visible

    def set_opacity(self, opacity: float):
        self.opacity = max(0.0, min(1.0, opacity))

    def clear(self):
        if self.image:
            # Clear to transparent
            self.image = Image.new("RGBA", self.image.size, (0, 0, 0, 0))
            self.draw_context = ImageDraw.Draw(self.image)


class LayerManager:
    """
    Mengelola banyak lapisan gambar, termasuk penambahan, penghapusan,
    pengurutan, dan penggabungan.
    """

    def __init__(self, app_instance, canvas_width: int, canvas_height: int):
        self.app = app_instance
        self.layers = []
        self.active_layer_index = -1
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self._add_initial_layer()
        print("LayerManager diinisialisasi.")

    def _add_initial_layer(self):
        """Menambahkan layer pertama (latar belakang) secara otomatis."""
        initial_layer = Layer(self.canvas_width, self.canvas_height, name="Background",
                              background_color="#FFFFFFFF")  # Latar belakang putih buram
        self.layers.append(initial_layer)
        self.active_layer_index = 0
        print("Layer 'Background' ditambahkan.")

    def add_layer(self, name: str = "New Layer"):
        """
        Menambahkan lapisan baru.
        """
        new_layer = Layer(self.canvas_width, self.canvas_height, name)
        self.layers.append(new_layer)
        # Set layer baru sebagai aktif
        self.active_layer_index = len(self.layers) - 1
        print(f"Layer '{name}' ditambahkan. Total layer: {len(self.layers)}")
        self.app.main_window.update_status(f"Layer '{name}' ditambahkan.")
        # Pemicu pembaruan UI daftar layer

    def remove_layer(self, index: int):
        """
        Menghapus lapisan pada indeks tertentu.
        """
        if 0 <= index < len(self.layers):
            if len(self.layers) > 1:  # Pastikan selalu ada setidaknya satu layer
                removed_layer = self.layers.pop(index)
                print(f"Layer '{removed_layer.name}' dihapus.")
                # Sesuaikan active_layer_index jika layer aktif dihapus
                if self.active_layer_index >= len(self.layers):
                    self.active_layer_index = len(self.layers) - 1
                elif self.active_layer_index > index:
                    self.active_layer_index -= 1

                self.app.main_window.update_status(
                    f"Layer '{removed_layer.name}' dihapus.")
                # Pemicu pembaruan UI daftar layer
            else:
                print("Tidak dapat menghapus layer terakhir.")
                self.app.main_window.update_status(
                    "Tidak dapat menghapus layer terakhir.")
        else:
            print(f"Indeks layer {index} tidak valid untuk dihapus.")

    def set_active_layer(self, index: int):
        """
        Mengatur lapisan aktif untuk menggambar.
        """
        if 0 <= index < len(self.layers):
            self.active_layer_index = index
            print(f"Layer aktif diatur ke: {self.layers[index].name}")
            self.app.main_window.update_status(
                f"Layer aktif: {self.layers[index].name}")
            # Pemicu pembaruan UI daftar layer

    def get_active_layer(self) -> Layer:
        """
        Mengembalikan objek lapisan aktif.
        """
        if self.layers and 0 <= self.active_layer_index < len(self.layers):
            return self.layers[self.active_layer_index]
        return None

    def merge_layers(self, layer_index_top: int, layer_index_bottom: int):
        """
        Menggabungkan layer_index_top ke layer_index_bottom.
        """
        if not (0 <= layer_index_top < len(self.layers) and 0 <= layer_index_bottom < len(self.layers)):
            print("Indeks layer tidak valid untuk penggabungan.")
            return

        if layer_index_top == layer_index_bottom:
            print("Tidak bisa menggabungkan layer ke dirinya sendiri.")
            return

        # Pastikan layer_index_top di atas layer_index_bottom
        if layer_index_top < layer_index_bottom:
            layer_index_top, layer_index_bottom = layer_index_bottom, layer_index_top

        top_layer = self.layers[layer_index_top]
        bottom_layer = self.layers[layer_index_bottom]

        if not top_layer.is_visible:
            print(
                f"Layer {top_layer.name} tidak terlihat, tidak akan digabungkan.")
            return

        try:
            # Komposit top_layer ke bottom_layer
            # Alpha_composite digunakan untuk menangani transparansi
            bottom_layer.image.alpha_composite(top_layer.image)

            # Hapus layer atas setelah digabungkan
            self.remove_layer(layer_index_top)
            print(
                f"Layer '{top_layer.name}' digabungkan ke '{bottom_layer.name}'.")
            self.app.main_window.update_status(
                f"Layer digabungkan: {top_layer.name} -> {bottom_layer.name}.")
            # Pemicu pembaruan UI daftar layer
        except Exception as e:  # Tangani semua Exception, termasuk ImportError jika PIL belum diimpor
            print(
                f"Error saat menggabungkan layer: {e}. Pastikan Pillow (PIL) terinstal.")

    def get_composite_image(self):
        """
        Menggabungkan semua lapisan yang terlihat menjadi satu gambar komposit.
        """
        try:
            # from PIL import Image # Impor sudah di atas
            if not self.layers:
                return None

            # Mulai dengan gambar kosong transparan
            composite_image = Image.new(
                "RGBA", (self.canvas_width, self.canvas_height), (0, 0, 0, 0))

            for layer in self.layers:
                if layer.is_visible and layer.image:
                    # Gabungkan layer ke gambar komposit
                    # PIL's alpha_composite handles opacity if images are RGBA
                    composite_image = Image.alpha_composite(
                        composite_image, layer.image)

            # Konversi kembali ke RGB untuk kanvas Tkinter jika diperlukan
            return composite_image.convert("RGB")
        except Exception as e:  # Tangani semua Exception, termasuk ImportError jika PIL belum diimpor
            print(
                f"Error saat membuat gambar komposit: {e}. Pastikan Pillow (PIL) terinstal.")
            return None
