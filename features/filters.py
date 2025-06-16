# features/filters.py

# Import pustaka yang mungkin diperlukan untuk filter gambar
# Dipindahkan ke atas
from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageDraw


class ImageFilters:
    """
    Kumpulan fungsi untuk menerapkan berbagai filter gambar.
    """

    def __init__(self, app_instance):
        self.app = app_instance
        print("ImageFilters diinisialisasi.")

    def apply_filter(self, filter_name: str, **kwargs):
        """
        Menerapkan filter ke gambar aktif pada kanvas.
        """
        current_image = self.app.canvas_manager.current_image
        if not current_image:
            print("Tidak ada gambar untuk diterapkan filter.")
            self.app.main_window.update_status(
                "Tidak ada gambar untuk filter.")
            return

        try:
            # from PIL import Image, ImageFilter, ImageOps, ImageEnhance # Impor sudah di atas

            # Simpan keadaan sebelum filter untuk undo
            self.app.canvas_manager._add_to_history()

            processed_image = current_image.copy()

            if filter_name == "grayscale":
                processed_image = ImageOps.grayscale(processed_image)
                print("Filter: Grayscale diterapkan.")
            elif filter_name == "sepia":
                # Implementasi sederhana sepia
                pixels = processed_image.load()
                for i in range(processed_image.size[0]):
                    for j in range(processed_image.size[1]):
                        r, g, b = pixels[i, j]
                        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                        tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                        pixels[i, j] = (min(255, tr), min(
                            255, tg), min(255, tb))
                print("Filter: Sepia diterapkan.")
            elif filter_name == "blur":
                radius = kwargs.get("radius", 2)
                processed_image = processed_image.filter(
                    ImageFilter.GaussianBlur(radius))
                print(f"Filter: Blur (Radius: {radius}) diterapkan.")
            elif filter_name == "sharpen":
                processed_image = processed_image.filter(ImageFilter.SHARPEN)
                print("Filter: Sharpen diterapkan.")
            elif filter_name == "invert":
                processed_image = ImageOps.invert(processed_image)
                print("Filter: Invert diterapkan.")
            elif filter_name == "brightness":
                # >1.0 lebih cerah, <1.0 lebih gelap
                factor = kwargs.get("factor", 1.2)
                enhancer = ImageEnhance.Brightness(processed_image)
                processed_image = enhancer.enhance(factor)
                print(f"Filter: Brightness (Factor: {factor}) diterapkan.")
            elif filter_name == "contrast":
                factor = kwargs.get("factor", 1.2)
                enhancer = ImageEnhance.Contrast(processed_image)
                processed_image = enhancer.enhance(factor)
                print(f"Filter: Contrast (Factor: {factor}) diterapkan.")
            # Tambahkan lebih banyak filter di sini

            else:
                print(
                    f"Filter '{filter_name}' tidak dikenal atau belum diimplementasikan.")
                self.app.main_window.update_status(
                    f"Filter '{filter_name}' tidak dikenal.")
                # Hapus dari riwayat undo jika tidak ada filter yang diterapkan
                self.app.canvas_manager.undo_history.pop()
                return

            self.app.canvas_manager.current_image = processed_image
            # Perbarui drawing_context setelah gambar diubah
            self.app.canvas_manager.drawing_context = ImageDraw.Draw(
                self.app.canvas_manager.current_image)
            self.app.canvas_manager._update_canvas_display()
            self.app.main_window.update_status(
                f"Filter '{filter_name}' diterapkan.")

        except ImportError:
            print("Pillow (PIL) tidak terinstal, tidak dapat menerapkan filter gambar.")
            self.app.main_window.update_status(
                "Pillow tidak terinstal. Filter dibatalkan.")
            # Hapus dari riwayat undo jika PIL tidak ada
            self.app.canvas_manager.undo_history.pop()
        except Exception as e:
            print(f"Error saat menerapkan filter '{filter_name}': {e}")
            self.app.main_window.update_status(
                f"Error filter: {filter_name}. ({e})")
            # Hapus dari riwayat undo jika ada error
            self.app.canvas_manager.undo_history.pop()
