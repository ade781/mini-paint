# config.py

class AppConfig:
    """
    Kelas untuk menyimpan konfigurasi global aplikasi Paint.
    """
    # Pengaturan Jendela Utama
    WINDOW_TITLE = "Aplikasi Paint Kompleks"
    DEFAULT_WINDOW_WIDTH = 1024
    DEFAULT_WINDOW_HEIGHT = 768

    # Pengaturan Kanvas
    DEFAULT_CANVAS_WIDTH = 800
    DEFAULT_CANVAS_HEIGHT = 600
    DEFAULT_BACKGROUND_COLOR = "#FFFFFF"  # Putih

    # Pengaturan Alat Gambar (Drawing Tools)
    DEFAULT_BRUSH_SIZE = 5
    DEFAULT_BRUSH_COLOR = "#000000"  # Hitam
    ERASER_COLOR = "#FFFFFF"       # Penghapus akan menggambar dengan warna latar belakang
    MIN_BRUSH_SIZE = 1
    MAX_BRUSH_SIZE = 50

    # Pengaturan Undo/Redo
    MAX_UNDO_HISTORY = 20  # Jumlah langkah undo yang disimpan

    # Path Sumber Daya (Resources Paths) - Menghapus ICONS_PATH
    FONTS_PATH = "resources/fonts/"  # Tetap ada untuk font

    # Pengaturan Lainnya
    # Interval autosave dalam menit (jika diimplementasikan)
    AUTOSAVE_INTERVAL_MINUTES = 5

    # Contoh daftar warna standar untuk palet
    COLOR_PALETTE = [
        "#000000",  # Hitam
        "#FFFFFF",  # Putih
        "#FF0000",  # Merah
        "#00FF00",  # Hijau
        "#0000FF",  # Biru
        "#FFFF00",  # Kuning
        "#FF00FF",  # Magenta
        "#00FFFF",  # Cyan
        "#FFA500",  # Oranye
        "#800080",  # Ungu
        "#A52A2A",  # Coklat
        "#808080",  # Abu-abu
    ]

# Anda bisa menambahkan kelas konfigurasi lain jika diperlukan
# Misalnya, ToolConfig, LayerConfig, dll.
