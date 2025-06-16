# utils/color_utils.py

def hex_to_rgb(hex_color: str) -> tuple:
    """
    Mengonversi string warna heksadesimal (misal: "#RRGGBB") menjadi tuple RGB (R, G, B).

    Args:
        hex_color (str): String warna heksadesimal, harus dimulai dengan '#'.

    Returns:
        tuple: Tuple (R, G, B) di mana setiap nilai adalah integer antara 0 dan 255.

    Raises:
        ValueError: Jika format string heksadesimal tidak valid.
    """
    if not hex_color.startswith('#') or len(hex_color) != 7:
        raise ValueError(
            "Format heksadesimal tidak valid. Harap gunakan format '#RRGGBB'.")

    hex_color = hex_color[1:]  # Hapus '#'
    try:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return (r, g, b)
    except ValueError:
        raise ValueError(
            "Nilai heksadesimal tidak valid. Harap pastikan semua karakter adalah heksadesimal (0-9, A-F).")


def rgb_to_hex(rgb_color: tuple) -> str:
    """
    Mengonversi tuple RGB (R, G, B) menjadi string warna heksadesimal (misal: "#RRGGBB").

    Args:
        rgb_color (tuple): Tuple (R, G, B) di mana setiap nilai adalah integer antara 0 dan 255.

    Returns:
        str: String warna heksadesimal, dimulai dengan '#'.

    Raises:
        ValueError: Jika nilai RGB tidak valid (di luar rentang 0-255).
    """
    r, g, b = rgb_color
    if not all(0 <= c <= 255 for c in [r, g, b]):
        raise ValueError("Nilai RGB harus dalam rentang 0 hingga 255.")

    return f"#{r:02x}{g:02x}{b:02x}".upper()

# Anda bisa menambahkan fungsi utilitas warna lainnya di sini,
# seperti konversi HSV, operasi blending, dll.
